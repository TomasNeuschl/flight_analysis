from django import forms
from django.contrib import admin

from flight_analysis.settings import INFLUXDB_HOST, INFLUXDB_PORT, INFLUXDB_DATABASE
from flight_data.models.flight import Flight
from flight_data.models.status import Status
from flight_data.models.telemetry import Telemetry
from flight_data.services.Influx_service import InfluxService
from flight_data.services.csv_service import CSVService


class StatusInline(admin.TabularInline):
    model = Status

    def get_readonly_fields(self, request, obj=None):
        return ['csv_name']


class TelemetryInline(admin.TabularInline):
    model = Telemetry

    def get_readonly_fields(self, request, obj=None):
        return ['csv_name']


class FlightAdminForm(forms.ModelForm):
    status_file = forms.FileField(label='Status File', required=False)
    telemetry_file = forms.FileField(label='Telemetry File', required=False)

    class Meta:
        model = Flight
        fields = '__all__'

    def clean_status_file(self):
        status_file = self.cleaned_data.get('status_file')
        if status_file:
            self.check_if_csv_file(status_file)
        return status_file

    def clean_telemetry_file(self):
        telemetry_file = self.cleaned_data.get('telemetry_file')
        if telemetry_file:
            self.check_if_csv_file(telemetry_file)
        return telemetry_file

    @staticmethod
    def check_if_csv_file(file):
        if file.content_type != 'text/csv':
            raise forms.ValidationError('Invalid CSV file')


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    inlines = [StatusInline, TelemetryInline]
    form = FlightAdminForm

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        telemetry_csv_file = form.cleaned_data.get('telemetry_file')
        status_csv_file = form.cleaned_data.get('status_file')
        if telemetry_csv_file or status_csv_file:
            influx_service = InfluxService(
                host=INFLUXDB_HOST,
                port=INFLUXDB_PORT,
                database=INFLUXDB_DATABASE,
            )
            if telemetry_csv_file:
                telemetry_data = CSVService().parse_data(telemetry_csv_file)
                tags = {'telemetry_id': obj.telemetry.id}
                influx_service.delete_data('telemetry_data', 'telemetry_id', obj.telemetry.id)
                influx_service.write_data('telemetry_data', tags, telemetry_data)
                obj.telemetry.csv_name = telemetry_csv_file.name
                obj.telemetry.save()
            if status_csv_file:
                tags = {'status_id': obj.status.id}
                status_data = CSVService().parse_data(status_csv_file)
                influx_service.delete_data('status_data','status_id', obj.status.id)
                influx_service.write_data('status_data', tags, status_data)
                obj.status.csv_name = status_csv_file.name
                obj.status.save()

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)

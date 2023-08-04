# myapp/serializers.py

from rest_framework import serializers
from .models import Invoice, InvoiceDetail

class InvoiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDetail
        fields = ('id', 'description', 'quantity', 'unit_price', 'price')

class InvoiceSerializer(serializers.ModelSerializer):
    details = InvoiceDetailSerializer(many=True)  # Remove read_only=True

    class Meta:
        model = Invoice
        fields = ('id', 'date', 'invoice_no', 'customer_name', 'details')

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        invoice = Invoice.objects.create(**validated_data)
        for detail_data in details_data:
            InvoiceDetail.objects.create(invoice=invoice, **detail_data)
        return invoice

    def update(self, instance, validated_data):
        # Update the fields of the Invoice instance
        instance.date = validated_data.get('date', instance.date)
        instance.invoice_no = validated_data.get('invoice_no', instance.invoice_no)
        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.save()

        # Update the nested InvoiceDetail instances
        details_data = validated_data.get('details', [])
        existing_details = {detail.id: detail for detail in instance.details.all()}

        for detail_data in details_data:
            detail_id = detail_data.get('id')
            if detail_id:
                # If the detail_id is present, update the existing InvoiceDetail
                detail = existing_details.get(detail_id)
                if detail:
                    detail.description = detail_data.get('description', detail.description)
                    detail.quantity = detail_data.get('quantity', detail.quantity)
                    detail.unit_price = detail_data.get('unit_price', detail.unit_price)
                    detail.price = detail_data.get('price', detail.price)
                    detail.save()
            else:
                # If the detail_id is not present, create a new InvoiceDetail
                InvoiceDetail.objects.create(invoice=instance, **detail_data)

        # Delete any removed InvoiceDetail instances
        detail_ids_to_delete = set(existing_details.keys()) - {detail_data.get('id') for detail_data in details_data}
        InvoiceDetail.objects.filter(id__in=detail_ids_to_delete).delete()

        return instance
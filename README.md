### Vendor Management Sysytem ###

Overview:
 
This is a Vendor Management System developed using Django and Django REST Framework. The sysytem allows users to manage vendor profiles, track purchase orders, and calculate vendor performance metrics. It includes three core features: Vendor Profile Management, Purchase Order Tracking, and Vendor Performance Evaluation.

#Installation
    1) Make sure you have Python and pip installed on your system.

    2)Install the required dependencies:
        pip install -r requirements.txt

    3)Apply migrations to set up the database:
        python manage.py migrate

    4)Create a superuser account to access the Django Admin interface:
        python manage.py createsuperuser

    5)Run the development server:
        python manage.py runserver

    6)Access the admin interface at http://localhost:8000/admin/ and log in with the superuser credentials.


Core Features
    1. Vendor Profile Management
        -> Model Design: The Vendor model stores essential information about each vendor, including performance metrics.

        API Endpoints:

            --> POST /api/vendors/: Create a new vendor.
            
            --> GET /api/vendors/: List all vendors.
            
            --> GET /api/vendors/{vendor_id}/: Retrieve a specific vendor's details.
            
            --> PUT /api/vendors/{vendor_id}/: Update a vendor's details.
            
            --> DELETE /api/vendors/{vendor_id}/: Delete a vendor.

    2. Purchase Order Tracking
        -> Model Design: The PurchaseOrder model tracks purchase orders with various details.

        API Endpoints:

            --> POST /api/purchase_orders/: Create a purchase order.
            
            --> GET /api/purchase_orders/: List all purchase orders with an option to filter by vendor.
            
            --> GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.
            
            --> PUT /api/purchase_orders/{po_id}/: Update a purchase order.
            
            --> DELETE /api/purchase_orders/{po_id}/: Delete a purchase order.

    3. Vendor Performance Evaluation
        -> Metrics: The Vendor model includes fields to store performance metrics such as on-time delivery rate, quality rating, response time, and fulfillment rate.

        API Endpoint:

            --> GET /api/vendors/{vendor_id}/performance: Retrieve a vendor's performance metrics.



Data Models
    1. Vendor Model
        Fields:

            --> name: Vendor's name.
            
            --> contact_details: Contact information of the vendor.
            
            --> address: Physical address of the vendor.
            
            --> vendor_code: A unique identifier for the vendor.
            
            --> on_time_delivery_rate: Tracks the percentage of on-time deliveries.
            
            --> quality_rating_avg: Average rating of quality based on purchase orders.
            
            --> average_response_time: Average time taken to acknowledge purchase orders.
            
            --> fulfillment_rate: Percentage of purchase orders fulfilled successfully.

    2. Purchase Order (PO) Model
        Fields:

            --> po_number: Unique number identifying the PO.
            
            --> vendor: Link to the Vendor model.
            
            --> order_date: Date when the order was placed.
            
            --> delivery_date: Expected or actual delivery date of the order.
            
            --> items: Details of items ordered (JSONField).
            
            --> quantity: Total quantity of items in the PO.
            
            --> status: Current status of the PO (e.g., pending, completed, canceled).
            
            --> quality_rating: Rating given to the vendor for this PO (nullable).
            
            --> issue_date: Timestamp when the PO was issued to the vendor.
            
            --> acknowledgment_date: Timestamp when the vendor acknowledged the PO.

    3. Historical Performance Model
        Fields:

            --> vendor: Link to the Vendor model.
            
            --> date: Date of the performance record.
            
            --> on_time_delivery_rate: Historical record of the on-time delivery rate.
            
            --> quality_rating_avg: Historical record of the quality rating average.
            
            --> average_response_time: Historical record of the average response time.
            
            --> fulfillment_rate: Historical record of the fulfillment rate.


Backend Logic for Performance Metrics
    On-Time Delivery Rate
        --> Calculated each time a PO status changes to 'completed'.
        --> Count the number of completed POs delivered on or before the delivery_date and divide by the total number of completed POs for that vendor.

    Quality Rating Average
        --> Updated upon the completion of each PO where a quality_rating is provided.
        --> Calculate the average of all quality_rating values for completed POs of the vendor.

    Average Response Time
        --> Calculated each time a PO is acknowledged by the vendor.
        --> Compute the time difference between issue_date and acknowledgment_date for each PO, and find the average of these times for all POs of the vendor.
            
    Fulfilment Rate
        --> Calculated upon any change in PO status.
        --> Divide the number of successfully fulfilled POs (status 'completed' without issues) by the total number of POs issued to the vendor.
        

#API Endpoint Implementation

    Vendor Performance Endpoint (GET /api/vendors/{vendor_id}/performance):
        --> Retrieves the calculated performance metrics for a specific vendor.
        --> Returns data including on_time_delivery_rate, quality_rating_avg, average_response_time, and fulfillment_rate.

    Update Acknowledgment Endpoint:
        --> Consider an endpoint like POST /api/purchase_orders/{po_id}/acknowledge for vendors to acknowledge POs.
        --> This endpoint updates acknowledgment_date and triggers the recalculation of average_response_time.

    
Additional Technical Considerations:
    --> Efficient Calculation: Ensure that the logic for calculating metrics is optimized to handle large datasets without significant performance issues.
    --> Data Integrity: Include checks to handle scenarios like missing data points or division by zero in calculations.
    --> Real-time Updates: Consider using Django signals to trigger metric updates in real-time when related PO data is modified.


Technical Requirements:
    --> Use the latest stable version of Django and Django REST Framework.
    --> Adhere to RESTful principles in API design.
    --> Implement comprehensive data validations for models.
    --> Utilize Django ORM for database interactions.
    --> Secure API endpoints with token-based authentication.
    --> Follow PEP 8 style guidelines for Python code.
    --> Document each API endpoint thoroughly.


Conclusion
    This Vendor Management System provides a robust solution for handling vendor profiles, purchase order tracking, and performance evaluation. Follow the installation steps to set up the system and leverage the powerful features to manage vendors effectively. For any issues or improvements, feel free to contribute or reach out to the project maintainers.
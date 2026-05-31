### 1. Three-sentence specification

1. The program will help Sharma Tent House manage bookings, inventory, payments, returns, and damages.

2. The system will be used by Rakesh ji and Ankit to quickly check availability, create bookings, and track rented items.

3. The project will be considered complete when booking management, inventory tracking, payment handling, return processing, and data storage using JSON files are working correctly


## 2. The information your program must remember

The program needs to store customer details, inventory items, bookings, payments, returns, and damage information so that Sharma Tent House can continue work properly even after closing the program.

### Customers

This stores information about people who book events.

- customer_id - string - required
- 
- customer_name - string - required
- 
- phone_number - string - required
- 
- address - string - required
- 
- customer_type - string - optional
- 
- notes - string - optional

The notes field can be used for things like trusted customers, late payments, or special requests.

---

### Inventory Items

Stores the main inventory categories managed by Sharma Tent House. This includes both bulk-counted items like chairs and plates and uniquely tracked assets like LED walls and sofa sets.

- item_id - string - required  
  Unique identifier for each inventory item category.

- item_name - string - required  
  Name of the inventory item.

- category - string - required  
  Type of inventory item such as seating, lighting, catering, decoration, or electronics.

- total_quantity - integer - required  
  Total number of units owned by the business.

- available_quantity - integer - optional  
  Dynamically calculated quantity currently free for booking during a selected date range.

- tracking_type - string - required  
  Values: bulk or unique_unit.

- price_per_day - float - required  
  Default rental price charged per day.

- damage_fee_per_unit - float - optional  
  Standard deduction amount for lost or damaged units.

- current_status - string - optional  
  Used for overall inventory state such as active, low_stock, or discontinued.

- notes - string - optional  
  Stores extra operational information about the item.

 ### Individually Tracked Inventory Units

Used for high-value or uniquely identifiable assets like LED walls, imported sound systems, and decorative sofa sets.

- unit_id - string - required

- parent_item_id - string - required

- serial_label - string - optional

- current_status - string - required
- 
- current_booking_id - string - optional
  
- notes - string - optional

The tracking_type field determines how inventory is managed in the system. Bulk items like plastic chairs, tables, plates, and glasses are tracked using quantities, while high-value or uniquely identifiable assets like LED walls, imported sound systems, and decorative sofa sets require separate unit-level tracking through the Individually Tracked Inventory Units model.

---

### Bookings

This stores all booking information for events.

- booking_id - string - required
- 
- customer_id - string - required
- 
- event_name - string - required
- 
- event_address - string - required
- 
- event_start_date - date (YYYY-MM-DD) - required

- event_end_date - date (YYYY-MM-DD) - required
  
- dispatch_date - date (YYYY-MM-DD) - required
  
- expected_return_date - date (YYYY-MM-DD) - required
  
- actual_return_date - date (YYYY-MM-DD) - optional
 
- booking_status - string - required
- 
- deposit_amount - float - required
- 
- total_amount - float - required
- 
- booked_items - list - required
-
- payment_records - list - required

- damage_charges - list - optional

- late_return_charges - list - optional

- refund_amount - float - optional
 
One booking can contain many different items with different quantities.

The remaining balance is not stored directly. It is calculated dynamically using:
(total_amount + penalties) - payments - refunds.
This avoids inconsistencies between stored balances and transaction history.

---

### Booking Items

This stores the individual items inside a booking.

- item_id - string - required
- 
- quantity - integer - required
- 
- price_per_day - float - required
- 
- total_days - integer - required

- standard_price_per_day - float - required
  
- quoted_price_per_day - float - required
  Actual rate charged to customer after negotiations or discounts.

- discount_reason - string - optional
  Stores why the rate differs from standard price.

This helps in calculating the final booking amount.

---

### Payments

This stores payment records.

- payment_id - string - required
- 
- booking_id - string - required
- 
- payment_date - string - required
- 
- amount - float - required
- 
- payment_type - string - required
- 
- payment_method - string - optional

Payment type can be deposit payment, full payment, or remaining balance payment.

---

### Returns and Damages

This stores information about returned items.

- return_id - string - required
- 
- booking_id - string - required
- 
- returned_items - list - required
- 
- missing_items - list - optional
- 
- damaged_items - list - optional
- 
- late_days - integer - optional
- 
- extra_charges - float - optional

This section helps calculate late fees, missing item charges, and damage deductions from the deposit. 

### 3. How your groupings connect to each other.

Bookings are connected to inventory items because one booking can contain many different rental items like chairs, tables, fans, and decoration items.
Inventory availability is checked using booking date ranges instead of permanently reducing stock quantities. When a new booking request is made, the system compares its dispatch_date and expected_return_date against existing bookings for the same item.
For example, if 200 out of 500 chairs are booked for a wedding from 17 Dec to 20 Dec, those chairs are considered unavailable only during that time window. The same chairs can still be booked for another event next month because the booking periods do not overlap.

Customers are connected to bookings because every booking belongs to one customer.

Payments are connected to bookings because each booking can have deposit payments, balance payments, or extra charges for damages.

Returns and damages are also connected to bookings. When items are returned, the system checks whether all items came back correctly, whether any item is damaged, or whether anything is missing.

Inventory items are connected to returns and damages because damaged or missing items affect the available stock of that item.

The booking system depends on inventory availability. Before confirming a booking, the program checks whether enough quantity of each item is available for the selected dates.

Bookings connect to payment records, damage charges, and late-return charges. The system derives the current outstanding balance from these related records instead of storing a mutable remaining_amount field.

Bookings connect to inventory in two different ways:
bulk items reserve quantities across a date range, while uniquely tracked inventory units are assigned specific unit_ids to prevent the same physical asset from being promised to multiple events simultaneously.

### 4. file structure

The program will use separate JSON files instead of one large file. This will make the data easier to manage and reduce the chances of losing all records if one file gets corrupted.

### customers.json

```json

{

  "customers": [

    {

      "customer_id": "C101",

      "customer_name": "Rahul Agarwal",

      "phone_number": "9876543210",

      "address": "Talwandi, Kota",

      "customer_type": "regular",

      "notes": "Usually pays on time"

    }

  ]

}

### bookings.json

{

  "bookings": [

    {

      "booking_id": "B201",

      "customer_id": "C101",

      "event_type": "Wedding",

      "event_address": "Utsav Garden, Kunhadi, Kota",

      "dispatch_date": "2026-12-17",

      "event_start_date": "2026-12-18",

      "event_end_date": "2026-12-19",

      "expected_return_date": "2026-12-20",

      "booking_status": "active",

      "total_amount": 85000,

      "deposit_amount": 25000,

      "special_requests": "Need extra lighting near food stalls."

    }

  ]

}

"booked_items": [

{

"item_id": "ITEM101",

"quantity": 200,

"standard_price_per_day": 12,

"quoted_price_per_day": 10,

"total_days": 2,

"discount_reason": "Regular customer discount"

}

]

### Inventory_units.json

{

  "unit_id": "LED-WALL-01",
  
  "parent_item_id": "ITEM101",
  
  "current_booking_id": "BOOKING204"
  
}

### Payments.json

{

  "payments": [
  
    {
    
      "payment_id": "P301",
      
      "booking_id": "B201",

      "payment_date": "2026-11-10",

      "amount": 25000,
      
      "payment_method": "cash",

      "note": "Advance payment during booking."
      
    },

    {
      "payment_id": "P302",
      
      "booking_id": "B201",

      "payment_date": "2026-12-18",

      "amount": 40000,
      
      "payment_method": "UPI",

      "note": "Partial payment collected at delivery."
      
    }
    
  ]
  
}

If the business grows to around 5,000 bookings per year, the program may become slower because availability checks, customer history searches, and payment calculations would require scanning large JSON files repeatedly. Managing updates across multiple JSON files could also create consistency problems if the program closes unexpectedly while saving data.

At a larger scale, a proper database system with indexed searching and safer transaction handling would likely be more reliable than plain JSON storage.

### 5. Operations 

1. User creates a new booking → system checks item availability for selected dates → system shows booking confirmation and total amount.

2. User enters customer details → system stores customer information → system shows generated customer ID.

3. User adds rental items to a booking → system calculates total quantity and price → system updates booking summary.

4. User checks item availability → system compares booked quantities with available stock → system shows available or unavailable status.

5. User tries to book more items than available → system blocks the booking → system shows warning message.

6. User views all bookings → system loads booking records → system shows booking list.

7. User searches booking by customer name or booking ID → system finds matching records → system shows booking details.

8. User records deposit payment → system updates payment history → system shows remaining balance.

9. User adds full or partial payment → system updates total paid amount → system shows updated balance.

10. User views customer history → system loads previous bookings and payments → system shows customer records.

11. User marks items as delivered → system updates booking status → system shows delivery confirmation.

12. User records returned items → system updates inventory quantity → system shows return summary.

13. User records damaged items → system calculates damage charges → system shows extra charges.

14. User records missing items → system adds missing item penalty → system updates final amount.

15. User records late return → system calculates late fees → system shows updated payment amount.

16. User closes a booking → system checks whether all items are returned → system marks booking as completed.

17. User tries to close booking with pending items → system blocks closing process → system shows missing item warning.

18. User views items currently out for events → system checks active bookings → system shows rented items list.

19. User views all events for a specific date → system checks booking dates → system shows deliveries and returns for that day.

20. User adds new inventory items → system stores item details → system updates inventory records.

21. User updates item quantity after purchasing new stock → system updates total and available quantity → system shows updated inventory.

22. User views damaged item report → system loads damage records → system shows damaged items and charges.

23. User exits the program → system saves all updated data into JSON files → system closes safely.

### 6. Things that can go wrong

1. User tries to book more items than available → system blocks the booking and shows the remaining available quantity for the selected dates.

2. Two bookings overlap on the same date for the same inventory item → system checks date ranges and prevents conflicting bookings from being confirmed.

3. User enters invalid dates or incorrect date format → system rejects the input and asks the user to re-enter the date in YYYY-MM-DD format.

4. Customer returns fewer items than were delivered → system marks the booking as partially returned and keeps the missing items pending.

5. Returned items are damaged → system records the damage details and adds damage charges to the booking settlement.

6. User enters a negative quantity for booking or inventory update → system rejects the value and asks for a valid positive quantity.

7. Items are returned after the expected return date → system calculates late return charges based on the number of delayed days.

8. Inventory quantity becomes negative because of incorrect updates → system cancels the operation and displays an inventory inconsistency warning.

9. JSON file becomes corrupted or unreadable → system shows an error message and attempts to load the latest backup copy if available.

10. Item status is marked as maintenance and user tries to book it → system blocks the booking and shows that the item is temporarily unavailable.

11. User accidentally enters a duplicate customer phone number → system warns the user and displays possible existing customer records before creating a new one.

12. Customer record does not exist when creating a booking → system asks the user to create a new customer record before continuing with the booking.

### 7. Thing that I dont know yet

I am still unsure about the best way to handle last-minute booking changes. In real tent house work, customers often increase or decrease quantities one or two days before the event, so I need to think carefully about how the system should update inventory without affecting other bookings already confirmed.

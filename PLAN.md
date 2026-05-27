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

This stores all rental items available in the tent house.

- item_id - string - required
- 
- item_name - string - required
- 
- category - string - required
- 
- total_quantity - integer - required
- 
- available_quantity - integer - required
- 
- price_per_day - float - required
- 
- item_type - string - required
- 
- damage_charge - float - optional
- 
- status - string - optional

The item_type field is important because some items are counted in quantity like chairs and tables, while some expensive items like LED walls or sofa sets may need separate tracking.

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
Customers are connected to bookings because every booking belongs to one customer.

Bookings are connected to inventory items because one booking can contain many different rental items like chairs, tables, fans, and decoration items. The system will reduce available quantity when items are booked and increase it again after return.

Payments are connected to bookings because each booking can have deposit payments, balance payments, or extra charges for damages.

Returns and damages are also connected to bookings. When items are returned, the system checks whether all items came back correctly, whether any item is damaged, or whether anything is missing.

Inventory items are connected to returns and damages because damaged or missing items affect the available stock of that item.

The booking system depends on inventory availability. Before confirming a booking, the program checks whether enough quantity of each item is available for the selected dates.

Bookings connect to payment records, damage charges, and late-return charges. The system derives the current outstanding balance from these related records instead of storing a mutable remaining_amount field.

### 4. file structure

The program will use separate JSON files instead of one large file. This will make the data easier to manage and reduce the chances of losing all records if one file gets corrupted.

### customers.json

''' json
[

    {
        "customer_id": "C101",
        
        "customer_name": "Rahul Agarwal",
        
        "phone_number": "9876543210",
        
        "address": "Talwandi, Kota",
        
        "customer_type": "regular",
        
        "notes": "Usually pays on time"
        
    }
   
]

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
1. user tries to book more items than available.
 
2. two bookings overlap on the same date.
 
3. user may enter invalid dates.
   
4. customer returns fewer items than booked.
   
5. returned items are damaged.
 
6. user may enter neagtive quantity.
 
7. items are returned late.
 
8. inventory quantity becomes negative.
 
9. JSON file may get corrupted
 
10. Item status is under mainatainance and user tries to book it
 
11. user accidently enters duplicate customer phone number
 
12. the customer may not exist already

### 7. Thing that I dont know yet


I am still unsure about the best way to handle last-minute booking changes. In real tent house work, customers often increase or decrease quantities one or two days before the event, so I need to think carefully about how the system should update inventory without affecting other bookings already confirmed.

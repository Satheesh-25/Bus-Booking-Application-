import random
import time
from datetime import date, timedelta
import re
import qrcode
from PIL import Image
from fpdf import FPDF

# Step 1: Login
username = input("username: ")
password = input("password: ")

if password.isdigit() and len(password) >= 8:
    print("Welcome " + username)
else:
    print("Wrong password. Password must be at least 8 digits.")
    exit()

# Step 2: OTP (with delay)
print("Enter the OTP (wait 10 seconds):")
time.sleep(10)
X = random.randint(100000, 999999)
print("Your OTP is:", X)

y = int(input("Enter the OTP: "))
if X != y:
    print("❌ You are wrong! The correct OTP was:", X)
    exit()
print("✅ You are right!")

# Step 3: FROM location
from_location = input("Enter your FROM location: ").strip()
if not from_location:
    print("❌ You did not define your FROM location.")
    exit()

# Step 4: TO location
destinations = ["Trichy", "Bangalore", "Coimbatore", "Dindigul", "Madurai", "Tirunelveli", "Nagercoil"]
locations = {str(i + 1): dest for i, dest in enumerate(destinations)}

for _ in range(3):
    print("\nAvailable destinations:")
    for key, value in locations.items():
        print(f"{key}. {value}")

    choice = input("Enter your TO location choice (1-7): ").strip()
    if choice in locations:
        to_location = locations[choice]
        route = f"{from_location} → {to_location}"

        # Step 5: Travel date
        today = date.today()
        travel_dates = [today + timedelta(days=i) for i in range(5)]
        date_options = {str(i + 1): d for i, d in enumerate(travel_dates)}

        for _ in range(3):
            print("\nAvailable travel dates:")
            for key, d in date_options.items():
                print(f"{key}. {d}")

            date_choice = input("Choose your travel date (1-5): ").strip()
            if date_choice in date_options:
                travel_date = date_options[date_choice]

                # Step 6: Seat generation
                row = random.choice(['A', 'B', 'C', 'D'])
                seat = random.randint(1, 20)
                full_seat = f"{row}{seat}"

                # Step 7: Passenger info
                name = input("Passenger name: ").strip()
                gender = input("Enter your gender (Male/Female): ").strip().capitalize()
                if gender not in ['Male', 'Female']:
                    print("❌ Invalid gender.")
                    exit()

                age = input("Passenger age: ").strip()
                phone = input("Enter your phone number (10 digits): ").strip()
                if not (phone.isdigit() and len(phone) == 10):
                    print("❌ Invalid phone number.")
                    exit()

                email = input("Enter your email: ").strip()
                if '@' not in email:
                    print("❌ Invalid email. Must contain '@'")
                    exit()

                confirm = input("Do you want to confirm your booking? (yes/no): ").strip().lower()
                if confirm != "yes":
                    print("Booking cancelled.")
                    exit()

                # Step 8: Ticket info (route included)
                ticket_info = (
                    f"Passenger: {name}\n"
                    f"From     : {from_location}\n"
                    f"To       : {to_location}\n"
                    f"Route    : {route}\n"
                    f"Date     : {travel_date}\n"
                    f"Seat     : {full_seat}\n"
                    f"Gender   : {gender}\n"
                    f"Age      : {age}\n"
                    f"Phone    : {phone}\n"
                    f"Email    : {email}"
                )

                # Step 9: QR code
                qr = qrcode.make(ticket_info)
                qr.save("ticket_qr.png")
                print("🎟️ QR Code saved as ticket_qr.png")

                # Step 10: Show QR
                img = Image.open("ticket_qr.png")
                img.show()

                # Step 11: Save to .txt (with emojis)
                with open("ticket_details.txt", "w", encoding="utf-8") as file:
                    file.write("🚌🚌🚌 BUS TICKET 🚌🚌🚌\n")
                    file.write(ticket_info + "\n")
                    file.write("QR Code: ticket_qr.png\n")
                    file.write("Have a safe journey! 😊\n")
                print("📄 Ticket saved to 'ticket_details.txt'")

                # Step 12: Save to PDF (strip emojis)
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Times", size=14)
                with open("ticket_details.txt", "r", encoding="utf-8") as file:
                    for line in file:
                        safe_line = ''.join(c for c in line if ord(c) < 128)
                        pdf.cell(200, 10, txt=safe_line.strip(), ln=True)
                pdf.output("ticket_details.pdf")
                print("📑 Ticket also saved as 'ticket_details.pdf'")

                # Final output
                print("\n🚌🚌🚌 BUS TICKET 🚌🚌🚌")
                print(ticket_info)
                print("Have a safe journey! 😊")
                break
            else:
                print("❌ Invalid date choice.")
        else:
            print("❌ Too many invalid attempts for travel date.")
        break
    else:
        print("❌ Invalid destination choice.")
else:
    print("❌ Too many invalid attempts for destination.")

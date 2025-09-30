#File Ok - not updated from example
# admin.py  Original Form

'''
CREATING A NEW DATABASE
-----------------------
Read explanation here: https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/

In the terminal navigate to the project folder just above the miltontours package
Type 'python' to enter the python interpreter. You should see '>>>'
In python interpreter type the following (hitting enter after each line):
    from digitalTime import db, create_app
    app = create_app()
    with app.app_context():
        db.create_all()	
The database should be created. Exit python interpreter by typing:
    quit()
Use DB Browser for SQLite to check that the structure is as expected before 
continuing.

ENTERING DATA INTO THE EMPTY DATABASE
-------------------------------------

# Option 1: Use DB Browser for SQLite
You can enter data directly into the cities or tours table by selecting it in
Browse Data and clicking the New Record button. The id field will be created
automatically. However be careful as you will get errors if you do not abide by
the expected field type and length. In particular the DateTime field must be of
the format: 2020-05-17 00:00:00.000000

# Option 2: Create a database seed function in an Admin Blueprint
See below. This blueprint needs to be enabled in __init__.py and then can be 
accessed via http://127.0.0.1:5000/admin/dbseed/
Database constraints mean that it can only be used on a fresh empty database
otherwise it will error. This blueprint should be removed (or commented out)
from the __init__.py after use.

Use DB Browser for SQLite to check that the data is as expected before 
continuing.
'''

from flask import Blueprint
from . import db
from .models import Watch, Order, orderdetails

bp = Blueprint('admin', __name__, url_prefix='/admin/')   #new blueprint for admin, any routes have /admin as a prefix

# function to put some seed data in the database
@bp.route('/dbseed/')       #Once program hits the route dbseed it runds the data populating
def dbseed():
    
    watch1=Watch(shortDesc="Casio A120WE-1 Front Button Series Digital Watch",longDesc="Awesome 1980s cool design with a pop of colour.  Bold coloured front buttons for a retro-futuristic look. Stopwatch and alarm functionality. Dimensions: 40.7 x 33.5 × 9.4 mm Weight: 53g Resin/Chrome Plated Case and Bezel Stainless Steel Band with Adjustable Clasp Water Resistant Approx. battery life: 3 years on CR1616 Resin Glass Silver ion plated band Additional features: Stopwatch Alarm/hourly time signal LED backlight Calendar: Auto-calendar Accuracy: ±30 seconds per month  Regular timekeeping: Hour, minute, second, pm, month, date, day specification=Watch Strap Material: Stainless Steel Watch Strap Colour: Silver Gender: Men's Watch Case Colour: Silver Watch Dial Colour: Black",review="Bobby Brown 7 May 2024 Amazing Product I love the watch and wear it every day! Patti Smith 5 January 2020 Cool watch Bought it as a present",price=199,image='./images/Products/A120WE-1.png')
    watch2=Watch(shortDesc="G-Shock GM5600G-9 Stay Gold Watch",longDesc="Step out in unique style in this striking G-Shock GM5600G-9 Stay Gold Men’s Watch. A watch unlike any other, this digital G-Shock is tough, with maximum protection while also boasting the luxurious feel of a traditional gold watch. Embrace confidence and class with a staple gold watch without worrying about damage. Featuring a digital display with an alarm, time, and backlight, you really are ready for anything in this watch. 49.6×43.2×12.9mm Case Size 73g Weight Resin/Stainless steel Case and Bezel Resin Band Shock Resistant 200 Meters Water Resistant Approx. battery life: 2 years on CR2016 Mineral Glass Stopwatch Timer Alarm/hourly time signal Hourly time signal Multi-function alarm Flash alert: Flashes with buzzer that sounds for alarms, hourly time signals Light: Electro-luminescent backlight Calendar: Full auto-calendar (to year 2099) Accuracy: ±15 seconds per month, specification=WATCH STRAP MATERIAL: Resin WATCH STRAP COLOUR: Black GENDER: Mens WATCH CASE COLOUR: Gold WATCH DIAL COLOUR: Black",review="Bobby Brown 7 May 2024 Amazing Product I love the watch and wear it every day! Patti Smith 5 January 2020 Cool watch Bought it as a present",price=249,image='./images/Products/GM5600G-9.png')
    watch3=Watch(shortDesc="G-Shock DW5040RX-7 40th Anniversary Skeleton Remix Digital Watch",longDesc="G-SHOCK celebrates its 40th anniversary this year, 2023, having presented its rugged and toughness since 1983. To commemorate the occasion Casio have come out with a limited-edition collection, the G-SHOCK 40th Clear Remix series. Included in this series is the G-Shock DW5040RX-7 40th Anniversary Skeleton Remix Digital Mens Watch. The watch offers a see-through deconstructed design, the see-through design is presented in the band, case, dial, LCD, and buttons providing a behind the scenes view of the watches intricate design.  48.9 × 42.8 × 13.5mm Case Size  78g Weight  Stainless steel/Resin Case and Bezel Resin Band  Shock Resistant  200 Meters Water Resistant  Approx. battery life: 3 years on CR2016  Mineral Glass  Stopwatch Timer Alarm/hourly time signal LED backlight (Super Illuminator) Calendar: Full auto-calendar (to year 2099) Accuracy: ±15 seconds per month",specification="WATCH STRAP MATERIAL: Silicone  WATCH TYPE: Alarm, Digital GENDER: Mens",review="Bobby Brown 7 May 2024 Amazing Product I love the watch and wear it every day! Patti Smith 5 January 2020 Cool watch Bought it as a present",price=279,image='./images/Products/DW5040RX.png')
    watch4=Watch(shortDesc="Maxum X1901L3 You Right",longDesc="This Maxum You Right X1901L3 was made to withstand the elements. This timepiece is made with functionalities such as stopwatch, alarm, backlight, and 100m water resistant. Digital Display Silicone Strap 36mm Case Size 100 Meters Water Resistant WATER RESISTANCE: 100 Metres WATCH STRAP MATERIAL: Silicone WATCH TYPE: Alarm, Digital WATCH STRAP COLOUR: Pink GENDER: Womens WATCH CASE COLOUR: Pink",review="Bobby Brown 7 May 2024 Amazing Product I love the watch and wear it every day! Patti Smith 5 January 2020 Cool watch Bought it as a present",price=79,image='./images/Products/MW23104G03.png')
    watch5=Watch(shortDesc=" Casio Vintage A171WE-1A Stainless Steel Digital Watch",longDesc=" The Casio Vintage A171WE-1A Stainless Steel Digital Watch, boasting a sleek case size of 38.8 × 37.7 × 9.2mm and a lightweight of 46g. Its resin and chrome-plated case and bezel exude durability, complemented by a stainless-steel band with an adjustable clasp for a customized fit. With water resistance and a battery life of approximately 7 years on CR2016, it's designed for long-lasting wear. Featuring resin glass, it includes practical features like a stopwatch, alarm with hourly time signal, daily alarm, and auto-calendar. Maintaining an accuracy of ±30 seconds per month, it supports both 12/24-hour formats and offers regular timekeeping with hour, minute, second, PM, date, and day displays.  38.8 × 37.7 × 9.2mm Case Size 46g Weight Resin/Chrome plated Case and Bezel Stainless Steel Band Adjustable Clasp Water Resistant Approx. battery life: 7 years on CR2016 Resin Glass Stopwatch Alarm/hourly time signal Daily alarm Calendar: Auto-calendar (set at 28 days for February) Accuracy: ±30 seconds per month 12/24-hour format Regular timekeeping: Hour, minute, second, pm, date, day WATCH STRAP MATERIAL: Stainless Steel WATCH TYPE: Alarm, Digital Specification=WATCH STRAP COLOUR: Silver GENDER: Unisex WATCH CASE COLOUR: Silver Specification WATCH DIAL COLOUR: Black",review="Bobby Brown 7 May 2024 Amazing Product I love the watch and wear it every day! Patti Smith 5 January 2020 Cool watch Bought it as a present",price=139,image='./images/Products/ A171WE-1A.png')
    watch6=Watch(shortDesc=" Maxum MW23104G03 Raglan",longDesc=" Named in tribute to the iconic surf break, Raglan ensures you're always in sync with the waves. It seamlessly merges functionality with style, recognizing the pivotal role of timing in ocean pursuits. This Maxum tide watch, featuring a digital display, keeps you updated on the tides' rhythm. Constructed from sturdy 316L Marine Grade Stainless Steel, Raglan showcases a sleek 40mm case size. Teamed with a stainless-steel bracelet fastened by a deployment clasp, it offers both durability and sophistication. With a water resistance of 200 meters, Raglan is primed for any aquatic escapade. Digital 316L Marine Grade Stainless Steel Case 40mm Case Size Stainless Steel Bracelet 200 Meters Water Resistant Deployment Clasp Unisex Specification=WATCH STRAP MATERIAL: Gold Plated Stainless Steel WATCH TYPE: Analogue, Digital WATCH STRAP COLOUR: Gold GENDER: Unisex",review="Bobby Brown 7 May 2024 Amazing Product I love the watch and wear it every day! Patti Smith 5 January 2020 Cool watch Bought it as a present Patti Smith 5 January 2020 Cool watch Bought it as a present",price=79,image='/.images/Products/MW23104G03.png')
    watch7=Watch(shortDesc=" Timex LCA TW2U72500 Digital",longDesc=" The revival of the '80s is upon us! We are feeling nostalgic and could not resist delving into our vintage collection. This time, we have resurrected a digital watch from the late 1980s that captured our hearts. Presenting the Q Timex Reissue Digital LCA, featuring a liquid crystal analogue display that pays homage to the original design. While we have given it a modern twist with a gold-tone stainless steel case, we've preserved the retro charm with the pre-INDIGLO® single-bulb backlight. Get ready to embrace the throwback vibes! Digital 32.5mm Case Size Stainless Steel Case and Bracelet 30 Meters Water Resistant Specification=WATCH STRAP MATERIAL: Silicone WATCH TYPE: Digital WATCH STRAP COLOUR: Black GENDER: Unisex WATCH STRAP MATERIAL: Gold Plated Stainless Steel WATCH TYPE: Analogue, Digital WATCH STRAP COLOUR: Gold GENDER: Unisex",review="Bobby Brown 7 May 2024 Amazing Product I love the watch and wear it every day! Patti Smith 5 January 2020 Cool watch Bought it as a present",price=79,image='./images/Products/MW23104G03.png')
    watch8=Watch(shortDesc=" Timex TW5M60900 Activity Tracker",longDesc=" Introducing the Timex Activity and Step Tracker, your essential tool for elevating your wellness journey. With a stylish 40mm gold tone metal case and a comfortable black silicone strap, this watch blends fashion with functionality seamlessly. Designed to optimize every movement, it combines step and activity tracking technology with the convenience of our INDIGLO® backlight. With water resistance up to 30 meters, it's your reliable companion for daily health management. Whether you're hitting the gym or conquering daily tasks, this watch empowers you to reach your personal best with ease. Digital 40mm Case Size Silicone Strap Activity Tracker Step Tracker 30 Meters Water Resistant Specification=WATCH STRAP MATERIAL: Silicone WATCH TYPE: Digital WATCH STRAP COLOUR: Black GENDER: Unisex",review="Bobby Brown 7 May 2024 Amazing Product I love the watch and wear it every day! Patti Smith 5 January 2020 Cool watch Bought it as a present",price=149,image='./images/Products/ TW5M60900.png')

    
    # Populate Watch Table
    try:
        # Clear existing rows
        db.session.query(Watch).delete()
        db.session.add(watch1)
        db.session.add(watch2)
        db.session.add(watch3)
        db.session.add(watch4)
        db.session.add(watch5)
        db.session.add(watch6)
        db.session.add(watch7)
        db.session.add(watch8)
        db.session.commit()    

    except:
        return '<h1>There was an issue adding the Watches in dbseed function<h1>'
   

    # Orders Table
    try:
        # Clear existing rows
        db.session.query(Order).delete()
        deleteOrder = orderdetails.delete()
        db.session.execute(deleteOrder)
        db.session.commit()
        
    except:
        return '<h1>There was an error initialising Orders Table in dbseed function</h1>'

    return 'DATA LOADED'


quit()
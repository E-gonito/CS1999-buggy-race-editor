from flask import Flask, render_template, request, jsonify
import sqlite3 as sql
import re
app = Flask(__name__)


DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"

BUGGY_RACE_SERVER_URL = "http://rhul.buggyrace.net"
#------------------------------------------------------------
# the index page
#------------------------------------------------------------
@app.route('/')
def home():
   return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)

#------------------------------------------------------------
# creating a new buggy
#------------------------------------------------------------
@app.route('/new', methods = ['POST', 'GET'])
def create_buggy():
  if request.method == 'GET':

      con = sql.connect(DATABASE_FILE)
      con.row_factory = sql.Row
      cur = con.cursor()
      cur.execute("SELECT * FROM buggies")
      record = cur.fetchone();
      return render_template("buggy-form.html", buggy = record)

  elif request.method == 'POST':
    all_colours = ('black', 'silver', 'gray', 'white', 'maroon', 'red', 'purple', 'fuchsia', 'green', 'lime', 'olive',
                   'yellow', 'navy', 'blue', 'teal', 'aqua', 'orange', 'aliceblue', 'antiquewhite', 'aquamarine',
                   'azure,beige', 'bisque,blanchedalmond', 'blueviolet,brown', 'burlywood', 'cadetblue', 'chartreuse',
                   'chocolate,coral', 'cornflowerblue', 'cornsilk,crimson', 'cyan', 'darkblue,darkcyan',
                   'darkgoldenrod',
                   'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange',
                   'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray',
                   'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey',
                   'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'gainsboro', 'ghostwhite', 'gold',
                   'goldenrod', 'greenyellow', 'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki',
                   'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan',
                   'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightgrey', 'lightpink', 'lightsalmon',
                   'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow',
                   'limegreen', 'linen', 'magenta', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple',
                   'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred',
                   'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'oldlace', 'olivedrab',
                   'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip',
                   'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon',
                   'sandybrown', 'seagreen', 'seashell', 'sienna', 'skyblue', 'slateblue', 'slategray', 'slategrey',
                   'snow', 'springgreen', 'steelblue', 'tan', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat',
                   'whitesmoke', 'yellowgreen', 'rebeccapurple')
    msg=""
    # number of wheels
    qty_wheels = request.form['qty_wheels']
    if not qty_wheels.isdigit() or int(qty_wheels)<4 or int(qty_wheels)%2 != 0 :
      msg = "You have not entered a valid number of wheels, your input must be numbers only, even and greater than 4!"
      return render_template("buggy-form.html", msg=msg)
    # flag colour
    flag_color = request.form['flag_color']
    match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', flag_color)
    if flag_color not in all_colours and not match:
      msg = "You have not entered a correct CSS colour for the primary flag colour, please use a colour keyword such as 'red' or a correct RGB hex value like '#ff0000"
      return render_template("buggy-form.html", msg=msg)
    if flag_color == "":
        flag_color = 'white'
    #flag_color_secondary
    flag_color_secondary = request.form['flag_color_secondary']
    match2 = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', flag_color_secondary)
    if flag_color_secondary not in all_colours and not match2:
      msg = "You have not entered a correct CSS colour for the secondary flag colour, please use a colour keyword such as 'red' or a correct RGB hex value like '#ff0000"
      return render_template("buggy-form.html", msg=msg)
    #Flag's pattern
    flag_pattern = request.form['flag_pattern']
    #power_type
    power_type = request.form['power_type']
    #power_units
    power_units = request.form['power_units']
    if not power_units.isdigit() or int(power_units) < 1:
        msg = "You have entered a invalid unit for the Primary motive power units, it must be 1 or greater"
        return render_template("buggy-form.html", msg=msg)
    #aux_power_type
    aux_power_type = request.form['aux_power_type']
    #aux_power_units
    if aux_power_type == 'none':
        aux_power_units = 0
    else:
        aux_power_units = request.form['aux_power_units']
        if not aux_power_units.isdigit():
            msg = "You have entered a invalid unit for the Auxiliary motive power units, it must be 0 or greater"
            return render_template("buggy-form.html", msg=msg)
    #hamster_booster
    if power_type == 'hamster' or aux_power_type == 'hamster':
        hamster_booster = request.form['hamster_booster']
        if not hamster_booster.isdigit():
            msg = "You have entered a invalid number for the amount of hamster boosters, please insert a integer"
            return render_template("buggy-form.html", msg=msg)
    else:
        hamster_booster = 0
    #Type of tyres
    tyres = request.form['tyres']
    #number of tyres
    qty_tyres = request.form['qty_tyres']
    if not qty_tyres.isdigit() or int(qty_tyres) < int(qty_wheels):
        msg = "You have entered a invalid number for the amount of tyres, please insert a integer and make sure you don't have less tyres than wheels"
        return render_template("buggy-form.html", msg=msg)
    #armour
    armour = request.form['armour']
    #fireproof
    fireproof = request.form['fireproof']
    #insulated
    insulated = request.form['insulated']
    #antibiotic
    antibiotic = request.form['antibiotic']
    #banging
    banging = request.form['banging']
    #offense
    attack = request.form['attack']
    #qty_attacks
    qty_attacks = request.form['qty_attacks']
    if not qty_attacks.isdigit() or int(qty_attacks) < 0:
        msg = "You have entered a invalid number for the amount attacks, please enter a integer bigger than or equal to 0"
        return render_template("buggy-form.html", msg=msg)
    #algo
    algo = request.form['algo']

    try:
      with sql.connect(DATABASE_FILE) as con:
        cur = con.cursor()
        cur.execute(
           "UPDATE buggies set qty_wheels=?, flag_color=?, flag_color_secondary=?, flag_pattern=?, power_type=?, power_units=?, aux_power_type=?, aux_power_units=?, hamster_booster=?, tyres=?, qty_tyres=?, armour=?, fireproof=?, insulated=?, antibiotic=?, banging=?, attack=?, qty_attacks=?, algo=? WHERE id=?",
           (qty_wheels, flag_color, flag_color_secondary,flag_pattern, power_type, power_units, aux_power_type, aux_power_units, hamster_booster, tyres, qty_tyres, armour, fireproof, insulated, antibiotic, banging, attack, qty_attacks, algo, DEFAULT_BUGGY_ID)
         )
        con.commit()
        msg = "Record successfully saved"
    except:
      con.rollback()
      msg = "error in update operation"
    finally:
      con.close()
      return render_template("updated.html", msg = msg)

#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/buggy')
def show_buggies():
  con = sql.connect(DATABASE_FILE)
  con.row_factory = sql.Row
  cur = con.cursor()
  cur.execute("SELECT * FROM buggies")
  record = cur.fetchone();
  return render_template("buggy.html", buggy = record)

#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/new')
def edit_buggy():
  return render_template("buggy-form.html")


#------------------------------------------------------------
# get JSON from current record
#   this is still probably right, but we won't be
#   using it because we'll be dipping diectly into the
#   database
#------------------------------------------------------------
@app.route('/json')
def summary():
  con = sql.connect(DATABASE_FILE)
  con.row_factory = sql.Row
  cur = con.cursor()
  cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (DEFAULT_BUGGY_ID))
  return jsonify(
      {k: v for k, v in dict(zip(
        [column[0] for column in cur.description], cur.fetchone())).items()
        if (v != "" and v is not None)
      }
    )

#------------------------------------------------------------
# delete the buggy
#   don't want DELETE here, because we're anticipating
#   there always being a record to update (because the
#   student needs to change that!)
#------------------------------------------------------------
@app.route('/delete', methods = ['POST'])
def delete_buggy():
  try:
    msg = "deleting buggy"
    with sql.connect(DATABASE_FILE) as con:
      cur = con.cursor()
      cur.execute("DELETE FROM buggies")
      con.commit()
      msg = "Buggy deleted"
  except:
    con.rollback()
    msg = "error in delete operation"
  finally:
    con.close()
    return render_template("updated.html", msg = msg)


if __name__ == '__main__':
   app.run(debug = True, host="0.0.0.0")

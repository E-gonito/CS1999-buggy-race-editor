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
    #buggy_id
    buggy_id = request.form['id']
    c_power_list = ("fusion", "thermo", "solar", "wind")

    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    record = cur.fetchone();

    # number of wheels
    qty_wheels = request.form['qty_wheels']
    if not qty_wheels.isdigit() or int(qty_wheels)<4 or int(qty_wheels)%2 != 0 :
      msg = "You have not entered a valid number of wheels, your input must be numbers only, even and greater than 4!"
      return render_template("buggy-form.html", msg=msg, buggy = record)
    # flag colour
    flag_color = request.form['flag_color']
    match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', flag_color)
    if flag_color not in all_colours and not match:
      msg = "You have not entered a correct CSS colour for the primary flag colour, please use a colour keyword such as 'red' or a correct RGB hex value like '#ff0000"
      return render_template("buggy-form.html", msg=msg, buggy = record)
    if flag_color == "":
        flag_color = 'white'
    #flag_color_secondary
    flag_color_secondary = request.form['flag_color_secondary']
    match2 = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', flag_color_secondary)
    if flag_color_secondary not in all_colours and not match2:
      msg = "You have not entered a correct CSS colour for the secondary flag colour, please use a colour keyword such as 'red' or a correct RGB hex value like '#ff0000"
      return render_template("buggy-form.html", msg=msg, buggy = record)
    #Flag's pattern
    flag_pattern = request.form['flag_pattern']
    #power_type
    power_type = request.form['power_type']
    #power_units
    power_units = request.form['power_units']
    if not power_units.isdigit() or int(power_units) < 1:
        msg = "You have entered a invalid unit for the Primary motive power units, it must be 1 or greater"
        return render_template("buggy-form.html", msg=msg)
    if power_type in c_power_list and int(power_units) > 1:
        msg = "Solar panels, sailing rigs, Nuclear and Thermonuclear reactors do not have consumable power units, please enter 1 as your power unit"
        return render_template("buggy-form.html", msg=msg, buggy = record)
    #aux_power_type
    aux_power_type = request.form['aux_power_type']
    #aux_power_units
    if aux_power_type == 'none':
        aux_power_units = 0
    else:
        aux_power_units = request.form['aux_power_units']
        if not aux_power_units.isdigit():
            msg = "You have entered a invalid unit for the Auxiliary motive power units, it must be 0 or greater"
            return render_template("buggy-form.html", msg=msg, buggy = record)
    if aux_power_type in c_power_list and int(aux_power_units) > 1:
        msg = "Solar panels, sailing rigs, Nuclear and Thermonuclear reactors do not have consumable power units, please enter 1 as your power unit"
        return render_template("buggy-form.html", msg=msg, buggy = record)
    #hamster_booster
    if power_type == 'hamster' or aux_power_type == 'hamster':
        hamster_booster = request.form['hamster_booster']
        if not hamster_booster.isdigit():
            msg = "You have entered a invalid number for the amount of hamster boosters, please insert a integer"
            return render_template("buggy-form.html", msg=msg, buggy = record)
    else:
        hamster_booster = 0
    #Type of tyres
    tyres = request.form['tyres']
    #number of tyres
    qty_tyres = request.form['qty_tyres']
    if not qty_tyres.isdigit() or int(qty_tyres) < int(qty_wheels):
        msg = "You have entered a invalid number for the amount of tyres, please insert a integer and make sure you don't have less tyres than wheels"
        return render_template("buggy-form.html", msg=msg, buggy = record)
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
        return render_template("buggy-form.html", msg=msg, buggy = record)
    #algo
    algo = request.form['algo']

    #cost calculator
    total_cost = int(0)

    cost_dict = {"petrol": "4", "fusion": "400", "steam": "3", "bio": "5", "electric": "20", "rocket": "16",
                 "hamster": "3", "thermo": "300", "solar": "40", "wind": "20", "knobbly": "15", "slick": "10",
                 "steelband": "20", "reactive": "40", "maglev":"50", "none": "0", "wood": "40", "aluminium": "200",
                 "thinsteel": "100", "thicksteel": "200", "titanium": "290", "spike": "5", "flame": "20",
                 "charge": "28", "biohazard": "30", "banging":"42","fireproof":"70","insulated":"100","antibiotic":"90"}

    weight_dict = {"knobbly":"20" , "slick": "14", "steelband": "28", "reactive": "20", "maglev":"30", "wood": "100",
                   "aluminium": "50", "thinsteel": "200", "thicksteel": "400", "titanium": "300" , "spike": "10",
                   "flame": "12", "charge": "25", "biohazard": "10", "banging":"42", "petrol": "2", "fusion": "100",
                   "steam": "4", "bio": "2", "electric": "20", "rocket": "2", "hamster": "1", "thermo": "100",
                   "solar": "30", "wind": "30", "none":"0"}

    tyres_weight = int(weight_dict[tyres])*int(qty_tyres)
    power_weight = int(weight_dict[power_type])*int(power_units)
    aux_power_weight = int(weight_dict[aux_power_type]) * int(aux_power_units)
    attack_weight = int(weight_dict[attack]) * int(qty_attacks)

    if int(qty_tyres) > 4:
        weight_mtply2 = int(qty_tyres)-4
        weight_mtply3 = weight_mtply2*10
        weight_mtply = weight_mtply3+100
    else:
        weight_mtply = 1

    armour_preweight = (int(weight_dict[armour]) * int(qty_wheels)) * weight_mtply
    armour_weight = armour_preweight / 100

    total_weight = tyres_weight+power_weight+aux_power_weight+attack_weight+armour_weight

    if banging == "true":
        total_cost += 42
    if fireproof == "true":
        total_cost += 70
    if insulated == "true":
        total_cost += 100
    if antibiotic == "true":
        total_cost += 90
    if power_type in cost_dict:
        total_cost += int(cost_dict[power_type])*int(power_units)
    if aux_power_type in cost_dict:
        total_cost += int(cost_dict[aux_power_type])*int(aux_power_units)
    if tyres in cost_dict:
        total_cost += int(cost_dict[tyres])*int(qty_tyres)
    if attack in cost_dict:
        total_cost += int(cost_dict[attack])*int(qty_attacks)
    if armour in cost_dict:
        armour_precost = (int(cost_dict[armour])*int(qty_wheels))*weight_mtply
        armour_cost = armour_precost/100
        total_cost += int(armour_cost)
    if int(weight_mtply) == 1:
        total_cost += int(cost_dict[armour])*int(qty_tyres)

    try:
        qty_wheels = request.form['qty_wheels']
        flag_color = request.form['flag_color']
        flag_color_secondary = request.form['flag_color_secondary']
        flag_pattern = request.form['flag_pattern']
        power_type = request.form['power_type']
        power_units = request.form['power_units']
        aux_power_type = request.form['aux_power_type']
        aux_power_units = request.form['aux_power_units']
        hamster_booster = request.form['hamster_booster']
        tyres = request.form['tyres']
        armour = request.form['armour']
        fireproof = request.form['fireproof']
        insulated = request.form['insulated']
        antibiotic = request.form['antibiotic']
        banging = request.form['banging']
        attack = request.form['attack']
        qty_attacks = request.form['qty_attacks']
        algo = request.form['algo']
        total_cost = total_cost

        with sql.connect(DATABASE_FILE) as con:
            cur = con.cursor()
            if buggy_id.isdigit():
                cur.execute(
                "UPDATE buggies set qty_wheels=?, flag_color=?, flag_color_secondary=?, flag_pattern=?, power_type=?, power_units=?, aux_power_type=?, aux_power_units=?, hamster_booster=?, tyres=?, qty_tyres=?, armour=?, fireproof=?, insulated=?, antibiotic=?, banging=?, attack=?, qty_attacks=?, algo=?, total_cost=? WHERE id=?",
                (qty_wheels, flag_color, flag_color_secondary,flag_pattern, power_type, power_units, aux_power_type, aux_power_units, hamster_booster, tyres, qty_tyres, armour, fireproof, insulated, antibiotic, banging, attack, qty_attacks, algo, total_cost, buggy_id)
                )
            else:
                cur.execute(
                "INSERT INTO buggies (qty_wheels, flag_color, flag_color_secondary, flag_pattern, power_type, power_units, aux_power_type, aux_power_units, hamster_booster, tyres, qty_tyres, armour, fireproof, insulated, antibiotic, banging, attack, qty_attacks, algo, total_cost) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (qty_wheels, flag_color, flag_color_secondary, flag_pattern, power_type, power_units, aux_power_type, aux_power_units, hamster_booster, tyres, qty_tyres, armour, fireproof, insulated, antibiotic, banging, attack, qty_attacks, algo, total_cost))
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
  records = cur.fetchall();
  return render_template("buggy.html", buggies = records)


#------------------------------------------------------------
# a page for editing buggies
#------------------------------------------------------------
@app.route('/edit/<buggy_id>')
def edit_buggy(buggy_id):
  con = sql.connect(DATABASE_FILE)
  con.row_factory = sql.Row
  cur = con.cursor()
  cur.execute("SELECT * FROM buggies WHERE id=?", (buggy_id,))
  record = cur.fetchone();
  return render_template("buggy-form.html", buggy = record)


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

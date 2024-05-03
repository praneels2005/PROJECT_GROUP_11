import psycopg2
from config import config
from flask import Flask, render_template, request

# Connect to the PostgreSQL database server
def connect(query):
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the %s database...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('Connected.')
      
        # create a cursor
        cur = conn.cursor()
        
        # execute a query using fetchall()
        cur.execute(query)
        rows = cur.fetchall()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result from fetchall()
    return rows
 
# app.py
app = Flask(__name__)


# serve form web page
@app.route("/")
def form():
    return render_template('index.html')

# The following functions handle each form/button we need for the home page
@app.route('/birthweight-handler', methods=['POST'])
def birthweights():
    rows = connect("SELECT tag, birth_weight, DATE(birthweights.dob) FROM birthweights JOIN Goat ON birthweights.animal_id = Goat.animal_id WHERE EXTRACT(YEAR FROM birthweights.dob) = " + request.form['INPUT'] + ";")
    heads = ['Tag', 'Birth Weight', 'Birth Date']
    return render_template('results.html', rows=rows, heads=heads)

@app.route('/birthweight-handler2', methods=['POST'])
def birthweights2():
    rows = connect("SELECT ROUND(avg(CAST(birth_weight AS numeric)), 3) FROM birthweights WHERE EXTRACT(YEAR FROM dob) = " + request.form['INPUT'] + ";")
    heads = ['Year Average']
    return render_template('results.html', rows=rows, heads=heads)

@app.route('/birthweight-handler3', methods=['POST'])
def birthweights3():
    rows = connect("SELECT tag, birth_weight, DATE(birthweights.dob) FROM birthweights JOIN Goat ON birthweights.animal_id = Goat.animal_id WHERE tag = '" + request.form['INPUT'] + "';")
    heads = ['Tag', 'Birth Weight', 'Birth Date']
    return render_template('results.html', rows=rows, heads=heads)

@app.route('/birthweight-info', methods=['POST'])
def birthinfo():
    rows = connect("SELECT ROUND(avg(CAST(birth_weight AS numeric)), 3) FROM birthweights;")
    heads = ['Overall Average Birth Weight']
    return render_template('results.html', rows=rows, heads=heads)

@app.route('/birthweight-info2', methods=['POST'])
def birthinfo2():
    rows = connect("SELECT LEAST(wt1.round, wt2.round, wt3.round, wt4.round, wt5.round, wt6.round, wt7.round, wt8.round, wt9.round, wt10.round, wt11.round) FROM wt1, wt2, wt3, wt4, wt5, wt6, wt7, wt8, wt9, wt10, wt11;")
    heads = ['Low Average Birth Weight']
    return render_template('results.html', rows=rows, heads=heads)

@app.route('/birthweight-info3', methods=['POST'])
def birthinfo3():
    rows = connect("SELECT GREATEST(wt1.round, wt2.round, wt3.round, wt4.round, wt5.round, wt6.round, wt7.round, wt8.round, wt9.round, wt10.round, wt11.round) FROM wt1, wt2, wt3, wt4, wt5, wt6, wt7, wt8, wt9, wt10, wt11;")
    heads = ['High Average Birth Weight']
    return render_template('results.html', rows=rows, heads=heads)

@app.route('/birthweight-info4', methods=['POST'])
def birthinfo4():
    rows = connect("SELECT CAST(max AS numeric) - CAST(min AS numeric) AS median FROM minmax;")
    heads = ['Median Birth Weight']
    return render_template('results.html', rows=rows, heads=heads)



@app.route('/doebirthing', methods=['POST'])
def doebirths():
    rows = connect("SELECT doebirthing.tag, momage, DATE(momdob), Goat.tag AS kidtag, DATE(kiddob) FROM doebirthing JOIN Goat ON doebirthing.kid = Goat.animal_id WHERE EXTRACT(YEAR FROM kidDOB) = " + request.form['INPUT'] + ";")
    heads = ['Tag', 'Age', 'Brith Date', 'Kid Tag', 'Kid Birth Date']
    return render_template('results.html', rows=rows, heads=heads)

@app.route('/doebirthing2', methods=['POST'])
def doebirths2():
    rows = connect("SELECT ROUND(avg(momage), 3) FROM doebirthing JOIN Goat ON doebirthing.kid = Goat.animal_id WHERE EXTRACT(YEAR FROM kidDOB) = " + request.form['INPUT'] + ";")
    heads = ['Year Average']
    return render_template('results.html', rows=rows, heads=heads)

@app.route('/doebirthing3', methods=['POST'])
def doebirths3():
    rows = connect("SELECT doebirthing.tag, momage, DATE(momdob), Goat.tag AS kidtag, DATE(kiddob) FROM doebirthing JOIN Goat ON doebirthing.kid = Goat.animal_id WHERE doebirthing.tag = '" + request.form['INPUT'] + "';")
    heads = ['Tag', 'Age', 'Brith Date', 'Kid Tag', 'Kid Birth Date']
    return render_template('results.html', rows=rows, heads=heads)



@app.route('/kidamt-handler', methods=['POST'])
def kidamt():
    rows = connect("SELECT ROUND(avg(CAST(singleweights.birth_weight AS numeric)), 3) AS singleAVG FROM singleweights;")
    heads = ['Average Single Kid Weight']
    return render_template('results.html', rows=rows, heads=heads)

@app.route('/kidamt-handler2', methods=['POST'])
def kidamt2():
    rows = connect("SELECT ROUND(avg(CAST(twinweights.birth_weight AS numeric)), 3) AS twinAVG FROM twinweights;")
    heads = ['Average Twin Kid Weight']
    return render_template('results.html', rows=rows, heads=heads)

@app.route('/kidamt-handler3', methods=['POST'])
def kidamt3():
    rows = connect("SELECT ROUND(avg(CAST(tripletweights.birth_weight AS numeric)), 3) AS tripletAVG FROM tripletweights;")
    heads = ['Average Triplet Kid Weight']
    return render_template('results.html', rows=rows, heads=heads)



@app.route('/newoldwt-handler', methods=['POST'])
def newoldwt():
    rows = connect("SELECT tag, birth_weight FROM firstmomweights JOIN Goat ON kidid = animal_id;")
    heads = ['Tag', 'First Mom Kid Birth Weight']
    return render_template('results.html', rows=rows, heads=heads)

@app.route('/newoldwt-handler2', methods=['POST'])
def newoldwt2():
    rows = connect("SELECT tag, birth_weight FROM oldermomweights JOIN Goat ON kidid = animal_id;")
    heads = ['Tag', 'Older Mom Kid Birth Weight']
    return render_template('results.html', rows=rows, heads=heads)

@app.route('/newoldwt-handler3', methods=['POST'])
def newoldwt3():
    rows = connect("SELECT ROUND(avg(CAST(birth_weight AS numeric)), 3) FROM firstmomweights;")
    heads = ['Average First Mom Kid Birth Weight']
    return render_template('results.html', rows=rows, heads=heads)

@app.route('/newoldwt-handler4', methods=['POST'])
def newoldwt4():
    rows = connect("SELECT ROUND(avg(CAST(birth_weight AS numeric)), 3) FROM oldermomweights;")
    heads = ['Average Older Mom Kid Birth Weight']
    return render_template('results.html', rows=rows, heads=heads)



@app.route('/kidnumdif-handler', methods=['POST'])
def kidnumdif():
    rows = connect("SELECT tag, alpha_value FROM firstmomkidnum JOIN Goat ON firstmomkidnum.animal_id = Goat.animal_id;")
    heads = ['First Mom Tag', 'Kid Amount']
    return render_template('results.html', rows=rows, heads=heads)

@app.route('/kidnumdif2-handler', methods=['POST'])
def kidnumdif2():
    rows = connect("SELECT tag, alpha_value FROM oldermomkidnum JOIN Goat ON oldermomkidnum.animal_id = Goat.animal_id;")
    heads = ['Older Mom Tag', 'Kid Amount']
    return render_template('results.html', rows=rows, heads=heads)

@app.route('/kidnumdif3-handler', methods=['POST'])
def kidnumdif3():
    rows = connect("SELECT ROUND(avg(CASE WHEN alpha_value = '1 Single' THEN 1 WHEN alpha_value = '2 Twins' THEN 2 WHEN alpha_value = '3 Triplets' THEN 3 WHEN alpha_value = '4 Quads' THEN 4 END), 3) AS firstMomKidAmtAvg FROM firstmomkidnum;")
    heads = ['Average First Mom Kid Amount']
    return render_template('results.html', rows=rows, heads=heads)

@app.route('/kidnumdif4-handler', methods=['POST'])
def kidnumdif4():
    rows = connect("SELECT ROUND(avg(CASE WHEN alpha_value = '1 Single' THEN 1 WHEN alpha_value = '2 Twins' THEN 2 WHEN alpha_value = '3 Triplets' THEN 3 WHEN alpha_value = '4 Quads' THEN 4 END), 3) AS olderMomKidAmtAvg FROM oldermomkidnum;")
    heads = ['Average Older Mom Kid Amount']
    return render_template('results.html', rows=rows, heads=heads)



@app.route('/vaccine-handler', methods=['POST'])
def vaccine():
    rows = connect("SELECT tag, birth_weight AS kid_bw FROM vaccinelist JOIN Goat ON mom = animal_id WHERE vaccine = 872;")
    heads = ['Dam Tag - Lepto/vibrio', 'Kid Birth Weight']
    return render_template('results.html', rows=rows, heads=heads)
@app.route('/vaccine2-handler', methods=['POST'])
def vaccine2():
    rows = connect("SELECT tag, birth_weight AS kid_bw FROM vaccinelist JOIN Goat ON mom = animal_id WHERE vaccine = 737;")
    heads = ['Dam Tag - Chlamydia/lepto/vibr', 'Kid Birth Weight']
    return render_template('results.html', rows=rows, heads=heads)
@app.route('/vaccine3-handler', methods=['POST'])
def vaccine3():
    rows = connect("SELECT tag, birth_weight AS kid_bw FROM vaccinelist JOIN Goat ON mom = animal_id WHERE vaccine = 49;")
    heads = ['Dam Tag - 5 in 1 Vacc', 'Kid Birth Weight']
    return render_template('results.html', rows=rows, heads=heads)
@app.route('/vaccine4-handler', methods=['POST'])
def vaccine4():
    rows = connect("SELECT tag, birth_weight AS kid_bw FROM vaccinelist JOIN Goat ON mom = animal_id WHERE vaccine = 1111;")
    heads = ['Dam Tag - Chlamydia', 'Kid Birth Weight']
    return render_template('results.html', rows=rows, heads=heads)
@app.route('/vaccine5-handler', methods=['POST'])
def vaccine5():
    rows = connect("SELECT tag, birth_weight AS kid_bw FROM vaccinelist JOIN Goat ON mom = animal_id WHERE vaccine = 1252;")
    heads = ['Dam Tag - Ivermectin', 'Kid Birth Weight']
    return render_template('results.html', rows=rows, heads=heads)
@app.route('/vaccine6-handler', methods=['POST'])
def vaccine6():
    rows = connect("SELECT tag, birth_weight AS kid_bw FROM vaccinelist JOIN Goat ON mom = animal_id WHERE vaccine = 754;")
    heads = ['Dam Tag - DL', 'Kid Birth Weight']
    return render_template('results.html', rows=rows, heads=heads)
@app.route('/vaccine7-handler', methods=['POST'])
def vaccine7():
    rows = connect("SELECT tag, birth_weight AS kid_bw FROM vaccinelist JOIN Goat ON mom = animal_id WHERE vaccine = 796;")
    heads = ['Dam Tag - PMHQ INTRANASAL', 'Kid Birth Weight']
    return render_template('results.html', rows=rows, heads=heads)
@app.route('/vaccine8-handler', methods=['POST'])
def vaccine8():
    rows = connect("SELECT tag, birth_weight AS kid_bw FROM vaccinelist JOIN Goat ON mom = animal_id WHERE vaccine = 708;")
    heads = ['Dam Tag - CD AND T VACCINE', 'Kid Birth Weight']
    return render_template('results.html', rows=rows, heads=heads)


@app.route('/vaccine9-handler', methods=['POST'])
def vaccine9():
    rows = connect("SELECT ROUND(avg(CAST(birth_weight AS numeric)), 3) FROM vaccinelist WHERE vaccine = 872;")
    heads = ['Average Kid Birth Weight of Dams Vaccinated w/ Lepto/vibrio']
    return render_template('results.html', rows=rows, heads=heads)
@app.route('/vaccine10-handler', methods=['POST'])
def vaccine10():
    rows = connect("SELECT ROUND(avg(CAST(birth_weight AS numeric)), 3) FROM vaccinelist WHERE vaccine = 737;")
    heads = ['Average Kid Birth Weight of Dams Vaccinated w/ Chlamydia/lepto/vibr']
    return render_template('results.html', rows=rows, heads=heads)
@app.route('/vaccine11-handler', methods=['POST'])
def vaccine11():
    rows = connect("SELECT ROUND(avg(CAST(birth_weight AS numeric)), 3) FROM vaccinelist WHERE vaccine = 49;")
    heads = ['Average Kid Birth Weight of Dams Vaccinated w/ 5 in 1 Vacc']
    return render_template('results.html', rows=rows, heads=heads)
@app.route('/vaccine12-handler', methods=['POST'])
def vaccine12():
    rows = connect("SELECT ROUND(avg(CAST(birth_weight AS numeric)), 3) FROM vaccinelist WHERE vaccine = 1111;")
    heads = ['Average Kid Birth Weight of Dams Vaccinated w/ Chlamydia']
    return render_template('results.html', rows=rows, heads=heads)
@app.route('/vaccine13-handler', methods=['POST'])
def vaccine13():
    rows = connect("SELECT ROUND(avg(CAST(birth_weight AS numeric)), 3) FROM vaccinelist WHERE vaccine = 1252;")
    heads = ['Average Kid Birth Weight of Dams Vaccinated w/ Invermectin']
    return render_template('results.html', rows=rows, heads=heads)
@app.route('/vaccine14-handler', methods=['POST'])
def vaccine14():
    rows = connect("SELECT ROUND(avg(CAST(birth_weight AS numeric)), 3) FROM vaccinelist WHERE vaccine = 754;")
    heads = ['Average Kid Birth Weight of Dams Vaccinated w/ DL']
    return render_template('results.html', rows=rows, heads=heads)
@app.route('/vaccine15-handler', methods=['POST'])
def vaccine15():
    rows = connect("SELECT ROUND(avg(CAST(birth_weight AS numeric)), 3) FROM vaccinelist WHERE vaccine = 796;")
    heads = ['Average Kid Birth Weight of Dams Vaccinated w/ PMHQ INTRANASAL']
    return render_template('results.html', rows=rows, heads=heads)
@app.route('/vaccine16-handler', methods=['POST'])
def vaccine16():
    rows = connect("SELECT ROUND(avg(CAST(birth_weight AS numeric)), 3) FROM vaccinelist WHERE vaccine = 708;")
    heads = ['Average Kid Birth Weight of Dams Vaccinated w/ CD AND T VACCINE']
    return render_template('results.html', rows=rows, heads=heads)

@app.route('/vaccine17-handler', methods=['POST'])
def vaccine17():
    rows = connect("SELECT tag, birth_weight AS kid_bw FROM vaccinelist JOIN Goat ON mom = animal_id WHERE vaccine != 872 AND vaccine != 737 AND vaccine != 49 AND vaccine != 1111 AND vaccine != 1252 AND vaccine != 754 AND vaccine != 796 AND vaccine != 708;")
    heads = ['Dam Tag - No Vaccinations', 'Kid Birth Weight']
    return render_template('results.html', rows=rows, heads=heads)
@app.route('/vaccine18-handler', methods=['POST'])
def vaccine18():
    rows = connect("SELECT ROUND(avg(CAST(birth_weight AS numeric)), 3) FROM vaccinelist WHERE vaccine != 872 AND vaccine != 737 AND vaccine != 49 AND vaccine != 1111 AND vaccine != 1252 AND vaccine != 754 AND vaccine != 796 AND vaccine != 708;")
    heads = ['Average Kid Birth Weight of Unvaccinated Dams']
    return render_template('results.html', rows=rows, heads=heads)


# This button returns the user back to the home page if they are on the results page
@app.route('/return-home', methods=['POST'])
def returnhome():
    return render_template('index.html')

# handle query POST and serve result web page
@app.route('/query-handler', methods=['POST'])
def query_handler():
    rows = connect(request.form['query'])
    return render_template('results.html', rows=rows)

# main loop
if __name__ == '__main__':
    app.run(debug = True)

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = f"sqlite:///{os.path.join(project_dir, 'testestimation.db')}"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Estimation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tester_name = db.Column(db.String(50), nullable=False)
    feature_name = db.Column(db.String(100), nullable=False)
    writing_checks = db.Column(db.Float, nullable=False)
    execution_checks = db.Column(db.Float, nullable=False)
    execution_retests = db.Column(db.Float, nullable=False)
    estimate_testing = db.Column(db.Float, nullable=False)


@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        tester_name = request.form['tester_name']
        feature_name = request.form['feature_name']
        writing_checks = float(request.form['writing_checks'])
        execution_checks = float(request.form['execution_checks'])
        execution_retests = float(request.form['execution_retests'])

        estimate_test_scenario = writing_checks + execution_checks
        risks = 0.3 * (estimate_test_scenario + execution_retests)
        estimate_testing = estimate_test_scenario + execution_retests + risks

        new_estimation = Estimation(
            tester_name=tester_name,
            feature_name=feature_name,
            writing_checks=writing_checks,
            execution_checks=execution_checks,
            execution_retests=execution_retests,
            estimate_testing=estimate_testing
        )
        db.session.add(new_estimation)
        db.session.commit()

        result = estimate_testing

    estimations = Estimation.query.all()
    return render_template('index.html', result=result, estimations=estimations)


@app.route('/estimations')
def estimations():
    all_estimations = Estimation.query.order_by(Estimation.tester_name).all()

    grouped_estimations = {}
    for estimation in all_estimations:
        if estimation.tester_name in grouped_estimations:
            grouped_estimations[estimation.tester_name].append(estimation)
        else:
            grouped_estimations[estimation.tester_name] = [estimation]

    return render_template('estimations.html', grouped_estimations=grouped_estimations)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


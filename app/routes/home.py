# app/routes/home.py

from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models.estimation import Estimation

home_bp = Blueprint('home', __name__)


def calculate_estimation(writing_checks, execution_checks, execution_retests):
    estimate_test_scenario = writing_checks + execution_checks
    risks = 0.3 * (estimate_test_scenario + execution_retests)
    return estimate_test_scenario + execution_retests + risks


@home_bp.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        tester_name = request.form['tester_name']
        feature_name = request.form['feature_name']
        writing_checks = float(request.form['writing_checks'])
        execution_checks = float(request.form['execution_checks'])
        execution_retests = float(request.form['execution_retests'])

        estimate_testing = calculate_estimation(writing_checks, execution_checks, execution_retests)

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

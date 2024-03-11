
from flask import Blueprint, render_template, redirect, url_for
from app import db
from app.models.estimation import Estimation

estimations_bp = Blueprint('estimations', __name__)

@estimations_bp.route('/estimations')
def estimations():
    all_estimations = Estimation.query.order_by(Estimation.tester_name).all()

    grouped_estimations = {}
    for estimation in all_estimations:
        if estimation.tester_name in grouped_estimations:
            grouped_estimations[estimation.tester_name].append(estimation)
        else:
            grouped_estimations[estimation.tester_name] = [estimation]

    return render_template('estimations.html', grouped_estimations=grouped_estimations)

@estimations_bp.route('/delete/<int:id>')
def delete_estimation(id):
    estimation_to_delete = Estimation.query.get_or_404(id)
    db.session.delete(estimation_to_delete)
    db.session.commit()
    return redirect(url_for('estimations.estimations'))
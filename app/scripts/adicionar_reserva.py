from tabnanny import check
from flask import render_template, request, redirect, url_for, flash
from app.forms import AdicionarReserva
from app.models import Hotels, Addresses, Reservation, Rooms, Guest
from app import db


def adicionar_reserva(user_id):
    form = AdicionarReserva()
    hotel = Hotels.query.order_by(Hotels.created_at).first()
    rooms = Rooms.query.filter_by(hotel_id=hotel.id).order_by(Rooms.number)
    guests = Guest.query.filter_by(hotel_id=hotel.id).order_by(Guest.name)

    form.room_id.choices = [(room.id, room.number) for room in rooms]
    form.guest_id.choices = [(guest.id, guest.name) for guest in guests]

    if request.method == 'POST':
      if form.validate_on_submit():
          reservation = Reservation.query.filter((Reservation.room_id == form.room_id.data) & (Reservation.check_in.between(form.check_in.data,  form.check_out.data) | Reservation.check_out.between(form.check_in.data,  form.check_out.data))).all()
          if not reservation:
              r = Reservation(total_guests=form.total_guests.data,
                              payment_type=form.payment_type.data,
                              check_in=form.check_in.data,
                              check_out=form.check_out.data,
                              room_id=form.room_id.data,
                              guest_id=form.guest_id.data,
                              user_id=user_id)
                              
              db.session.add(r)
              db.session.commit()

              flash('Reserva cadastrado com sucesso!', 'success')
          else:
              flash('Esse quarto já possui uma reserva para essa data.', 'danger')

    return render_template('add_reserva.html',
                           form=form,
                           titulo='Adicionar Reserva'
                           )
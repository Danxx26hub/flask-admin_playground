from app.models import db, Album, Artist
from app import app
from flask import jsonify, Blueprint, current_app
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from wtforms.fields import SelectField
import logging


@app.route("/number/<int:num_id>")
def index(num_id):

    data = (
        db.session.execute(
            db.select(Album).where(Album.AlbumId > num_id).order_by(Album.AlbumId)
        )
        .scalars()
        .all()
    )

    data_as_dict = [obj.return_dict() for obj in data]
    print(data_as_dict)
    for item in data_as_dict:
        item.pop("_sa_instance_state", None)

    return jsonify(data_as_dict)


@app.route("/joined")
def joined():
    from sqlalchemy.orm import joinedload

    album = Album.query.options(joinedload(Album.artist)).get(8)
    print(album.artist.Name)
    return f"{album.artist.Name}"


# Admin views
##############################################################################


class MyAdminIndexView(AdminIndexView):

    def is_accessible(self):
        return True


class admin_album_view(ModelView):
    column_auto_select_related = True
    column_display_pk = True
    can_edit = True
    column_details_list = ["AlbumId", "Title"]
    can_view_details = True
    column_hide_backrefs = False
    column_display_all_relations = True
    column_list = ("AlbumId", "Title", "artist.Name")  # Show artist's Name in list
    form_columns = ("AlbumId", "Title", "ArtistId")  # Use 'ArtistId' field for the form

    def scaffold_form(self):
        form_class = super(admin_album_view, self).scaffold_form()

        with app.app_context():
            # Create a custom SelectField for artist with artist names as choices
            form_class.ArtistId = SelectField(
                "Artist",
                choices=[
                    (artist.ArtistId, artist.Name) for artist in Artist.query.all()
                ],
                coerce=int,  # Ensure that we store an integer (ArtistId)
            )
        return form_class

    def on_model_change(self, form, model, is_created):
        """
        Override this method to manually set the artist relationship correctly
        """
        artist_id = form.ArtistId.data  # Retrieve the selected ArtistId

        if artist_id:
            # Fetch the Artist instance using the selected ID
            artist = Artist.query.get(artist_id)
            if artist:
                model.artist = (
                    artist  # Set the artist relationship to the actual Artist object
                )
                logging.info(f"Assigned artist: {model.artist.Name} (ID: {artist_id})")
            else:
                model.artist = None
                logging.warning(f"Artist with ID {artist_id} not found")
        else:
            model.artist = None
            logging.warning("No artist selected")

        # Now proceed with the default behavior (populate other fields)
        super().on_model_change(form, model, is_created)

    page_size = 25


admin_blueprint = Blueprint("admin", __name__)

admin_panel = Admin(
    app,
    name="admin",
    template_mode="bootstrap4",
    url="/admin",
    index_view=MyAdminIndexView(),
)
admin_panel.add_view(admin_album_view(Album, db.session, category="Music"))

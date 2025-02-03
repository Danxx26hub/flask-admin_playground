from app import app
from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


class Employee(db.Model):
    __tablename__ = "employees"
    EmployeeId = db.Column(db.Integer, primary_key=True)
    LastName = db.Column(db.String(80))
    FirstName = db.Column(db.String(80))
    Title = db.Column(db.String(80))
    ReportsTo = db.Column(db.Integer, db.ForeignKey("employees.EmployeeId"))
    BirthDate = db.Column(db.Date)
    HireDate = db.Column(db.Date)
    Address = db.Column(db.String(120))
    City = db.Column(db.String(80))
    State = db.Column(db.String(80))
    Country = db.Column(db.String(80))
    PostalCode = db.Column(db.String(20))
    Phone = db.Column(db.String(80))
    Fax = db.Column(db.String(80))
    Email = db.Column(db.String(120))


class Customer(db.Model):
    __tablename__ = "customers"
    CustomerId = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(80))
    LastName = db.Column(db.String(80))
    Company = db.Column(db.String(80))
    Address = db.Column(db.String(120))
    City = db.Column(db.String(80))
    State = db.Column(db.String(80))
    Country = db.Column(db.String(80))
    PostalCode = db.Column(db.String(20))
    Phone = db.Column(db.String(80))
    Fax = db.Column(db.String(80))
    Email = db.Column(db.String(120))
    SupportRepId = db.Column(db.Integer, db.ForeignKey("employees.EmployeeId"))


class Invoice(db.Model):
    __tablename__ = "invoices"
    InvoiceId = db.Column(db.Integer, primary_key=True)
    CustomerId = db.Column(db.Integer, db.ForeignKey("customers.CustomerId"))
    InvoiceDate = db.Column(db.Date)
    BillingAddress = db.Column(db.String(120))
    BillingCity = db.Column(db.String(80))
    BillingState = db.Column(db.String(80))
    BillingCountry = db.Column(db.String(80))
    BillingPostalCode = db.Column(db.String(20))
    Total = db.Column(db.Float)


class InvoiceItem(db.Model):
    __tablename__ = "invoice_items"
    InvoiceLineId = db.Column(db.Integer, primary_key=True)
    InvoiceId = db.Column(db.Integer, db.ForeignKey("invoices.InvoiceId"))
    TrackId = db.Column(db.Integer, db.ForeignKey("tracks.TrackId"))
    UnitPrice = db.Column(db.Float)
    Quantity = db.Column(db.Integer)


# class artists(db.Model):
#     __tablename__ = 'artists'
#     ArtistId = db.Column(db.Integer, primary_key=True)
#     Name = db.Column(db.String(120))
#     albums = db.relationship('albums', back_populates='artists')

# class albums(db.Model):
#     __tablename__ = 'albums'
#     AlbumId = db.Column(db.Integer, primary_key=True)
#     Title = db.Column(db.String(120))
#     ArtistId = db.Column(db.Integer, db.ForeignKey('artists.ArtistId'))
#     artist = db.relationship('artists', back_populates='albums')


class Artist(db.Model):
    __tablename__ = "artists"
    ArtistId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(120))

    # Define the relationship: An artist has many albums
    # albums = db.relationship('Album', backref='artist', lazy='dynamic')


class Album(db.Model):
    __tablename__ = "albums"
    AlbumId = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(120))
    ArtistId = db.Column(db.Integer, db.ForeignKey("artists.ArtistId"))

    # Define the relationship: Each album has one artist
    artist = db.relationship(
        Artist,
        backref=db.backref("albums", uselist=True),
    )

    def return_dict(self):
        album_dict = self.__dict__.copy()
        album_dict["artist_name"] = self.artist.Name if self.artist else None
        return album_dict


class MediaType(db.Model):
    __tablename__ = "media_types"
    MediaTypeId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(120))


class Genre(db.Model):
    __tablename__ = "genres"
    GenreId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(120))


class Track(db.Model):
    __tablename__ = "tracks"
    TrackId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(120))
    AlbumId = db.Column(db.Integer, db.ForeignKey("albums.AlbumId"))
    MediaTypeId = db.Column(db.Integer, db.ForeignKey("media_types.MediaTypeId"))
    GenreId = db.Column(db.Integer, db.ForeignKey("genres.GenreId"))
    Composer = db.Column(db.String(120))
    Milliseconds = db.Column(db.Integer)
    Bytes = db.Column(db.Integer)
    UnitPrice = db.Column(db.Float)


class Playlist(db.Model):
    __tablename__ = "playlists"
    PlaylistId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(120))


class PlaylistTrack(db.Model):
    __tablename__ = "playlist_track"
    PlaylistId = db.Column(
        db.Integer, db.ForeignKey("playlists.PlaylistId"), primary_key=True
    )
    TrackId = db.Column(db.Integer, db.ForeignKey("tracks.TrackId"), primary_key=True)

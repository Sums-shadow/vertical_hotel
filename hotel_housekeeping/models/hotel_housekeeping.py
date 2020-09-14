# See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HotelHousekeeping(models.Model):
    _name = "hotel.housekeeping"
    _description = "Reservation"
    _rec_name = "room_no"

    current_date = fields.Date(
        "Date actuelle",
        required=True,
        index=True,
        states={"done": [("readonly", True)]},
        default=fields.Date.today,
    )
    clean_type = fields.Selection(
        [
            ("daily", "quotidien"),
            ("checkin", "Enregistrement"),
            ("checkout", "Check-Out"),
        ],
        "Type de nettoyage",
        required=True,
        states={"done": [("readonly", True)]},
    )
    room_no = fields.Many2one(
        "hotel.room",
        "No chambre",
        required=True,
        states={"done": [("readonly", True)]},
        index=True,
    )
    activity_line_ids = fields.One2many(
        "hotel.housekeeping.activities",
        "a_list",
        "Activities",
        states={"done": [("readonly", True)]},
        help="Detail of housekeeping" "activities",
    )
    inspector_id = fields.Many2one(
        "res.users",
        "Inspecteur",
        required=True,
        index=True,
        states={"done": [("readonly", True)]},
    )
    inspect_date_time = fields.Datetime(
        "Inspection Date & heure",
        required=True,
        states={"done": [("readonly", True)]},
    )
    quality = fields.Selection(
        [
            ("excellent", "Excellente"),
            ("good", "Bonne"),
            ("average", "Moyenne"),
            ("bad", "Mauvaise"),
            ("ok", "Ok"),
        ],
        "Qualité",
        states={"done": [("readonly", True)]},
        help="Inspector inspect the room and mark \
                                as Excellent, Average, Bad, Good or Ok. ",
    )
    state = fields.Selection(
        [
            ("inspect", "Inspecter"),
            ("dirty", "Sale"),
            ("clean", "Propre"),
            ("done", "Fait"),
            ("cancel", "Annulé"),
        ],
        "State",
        states={"done": [("readonly", True)]},
        index=True,
        required=True,
        readonly=True,
        default="inspect",
    )

    
    def action_set_to_dirty(self):
        """
        This method is used to change the state
        to dirty of the hotel housekeeping
        ---------------------------------------
        @param self: object pointer
        """
        self.write({"state": "dirty", "quality": False})
        self.activity_line_ids.write({"clean": False, "dirty": True})

    
    def room_cancel(self):
        """
        This method is used to change the state
        to cancel of the hotel housekeeping
        ---------------------------------------
        @param self: object pointer
        """
        self.write({"state": "cancel", "quality": False})

    
    def room_done(self):
        """
        This method is used to change the state
        to done of the hotel housekeeping
        ---------------------------------------
        @param self: object pointer
        """
        if not self.quality:
            raise ValidationError(_("Veuillez mettre à jour la qualité du travail!"))
        self.state = "done"

    
    def room_inspect(self):
        """
        This method is used to change the state
        to inspect of the hotel housekeeping
        ---------------------------------------
        @param self: object pointer
        """
        self.write({"state": "inspect", "quality": False})

    
    def room_clean(self):
        """
        This method is used to change the state
        to clean of the hotel housekeeping
        ---------------------------------------
        @param self: object pointer
        """
        self.write({"state": "clean", "quality": False})
        self.activity_line_ids.write({"clean": True, "dirty": False})

# See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HotelHousekeepingActivities(models.Model):
    _name = "hotel.housekeeping.activities"
    _description = "Housekeeping Activities "

    a_list = fields.Many2one("hotel.housekeeping", string="Reservation")
    today_date = fields.Date("Date actuelle")
    activity_name = fields.Many2one(
        "hotel.activity", string="Activité d'entretien ménager"
    )
    housekeeper_id = fields.Many2one(
        "res.users", string="Gouvernant", required=True
    )
    clean_start_time = fields.Datetime("Heure de début de nettoyage", required=True)
    clean_end_time = fields.Datetime("Date de la fin de nrettoyage", required=True)
    dirty = fields.Boolean(
        "Sale",
        help="Vérifié si l'activité d'entretien ménager est sale.",
    )
    clean = fields.Boolean(
        "Propre",
        help="Vérifié si l’activité de nettoyage  est propre.",
    )

    @api.constrains("clean_start_time", "clean_end_time")
    def _check_clean_start_time(self):
        """
        This method is used to validate the clean_start_time and
        clean_end_time.
        ---------------------------------------------------------
        @param self: object pointer
        @return: raise warning depending on the validation
        """
        if self.clean_start_time >= self.clean_end_time:
            raise ValidationError(
                _("La date de début doit être inférieure à la date de fin!")
            )

    @api.model
    def default_get(self, fields):
        """
        To get default values for the object.
        @param self: The object pointer.
        @param fields: List of fields for which we want default values
        @return: A dictionary which of fields with values.
        """
        if self._context is None:
            self._context = {}
        res = super().default_get(fields)
        if self._context.get("room_id", False):
            res.update({"room_id": self._context["room_id"]})
        if self._context.get("today_date", False):
            res.update({"today_date": self._context["today_date"]})
        return res

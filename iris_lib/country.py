from django.utils.translation import ugettext_lazy as _
from django.db import models
import iso3166

# Common country names that depart from the ISO standard
# Note that these shouldn't change the sorting (they are generally just truncated versions of the full name)
COUNTRY_COMMON_NAMES = {
    "BN": _(u"Brunei"),
    "BO": _(u"Bolivia"),
    "IR": _(u"Iran"),
    "KP": _(u"Korea, North"),
    "KR": _(u"Korea, South"),
    "LA": _(u"Laos"),
    "MD": _(u"Moldova"),
    "MK": _(u"Macedonia"),
    "SY": _(u"Syria"),
    "TW": _(u"Taiwan"),
    "TZ": _(u"Tanzania"),
    "VE": _(u"Venezuela"),
    "VN": _(u"Vietnam"),

    # Other entities, these are reserved in the ISO3166 spec but not officially listed
    "UN": _(u"United Nations"),
    "EU": _(u"European Union"),

    # Multiple countries
    "M7": _(u"Multiple Countries"),
}


def get_country_name(country_code):
    # Common name if it exists
    if country_code in COUNTRY_COMMON_NAMES:
        return COUNTRY_COMMON_NAMES[country_code]
    # iso3166 country if it exists
    country = iso3166.countries.get(country_code, None)
    if country:
        return _(country.name)
    # Otherwise, return the code itself
    return country_code


# Make a choice list, with US at the top and otherwise sorted by name
COUNTRIES = [("US", get_country_name("US"))] + [
    (country.alpha2, get_country_name(country.alpha2))
    for country in iso3166.countries
    if country.alpha2 != "US"
]


class CountryField(models.CharField):

    description = "A field of countries"

    __metaclass__ = models.SubfieldBase

    def __init__(self, include_orgs=False, include_multiple=False, *args, **kwargs):

        COUNTRY_HELP_TEXT = " ".join([
            'Country names and codes based on the',
            '<a href="http://en.wikipedia.org/wiki/ISO_3166-1" target="_blank">',
            'ISO 3166 standard</a>.'
        ])

        choices = COUNTRIES
        if include_orgs:
            choices += [(code, get_country_name(code)) for code in ["UN", "EU"]]
        if include_multiple:
            choices += [(code, get_country_name(code)) for code in ["M7"]]

        kwargs.setdefault('max_length', 2)
        kwargs.setdefault('choices', choices)
        kwargs.setdefault('help_text', COUNTRY_HELP_TEXT)

        super(CountryField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"


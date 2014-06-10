App.CountryAdapter = App.ApplicationAdapter.extend({
    pathForType: function () {
        return 'geo/countries';
    }
});
App.Country = DS.Model.extend({
    name: DS.attr('string'),
    code: DS.attr('string'),
    oda: DS.attr('boolean')
});

App.UsedCountryAdapter = App.ApplicationAdapter.extend({
    pathForType: function () {
        return 'geo/used_countries';
    }
});
App.UsedCountry = App.Country.extend();
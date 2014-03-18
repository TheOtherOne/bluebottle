// Make sure we (de)serialize 'date' attributes the right way.
// DRF2 expects yyy-mm-ddThh:ii:ssZ
// Ember wants an js Date()
App.DateTransform = DS.Transform.extend({
    deserialize: function (serialized) {
        if (serialized == undefined) {
            return null;
        }
        return new Date(serialized);
    },

    serialize: function (date) {
        if (date == null) {
            return null;
        }
        var pad = function (num) {
            return num < 10 ? "0" + num : "" + num;
        };

        var utcYear = date.getUTCFullYear(),
            utcMonth = date.getUTCMonth() +1,
            utcDayOfMonth = date.getUTCDate(),
            utcDay = date.getUTCDay(),
            utcHours = date.getUTCHours(),
            utcMinutes = date.getUTCMinutes(),
            utcSeconds = date.getUTCSeconds();

        return utcYear + "-" + pad(utcMonth) + "-" + pad(utcDayOfMonth) + "T" + pad(utcHours) + ":" + pad(utcMinutes) + ":" + pad(utcSeconds) + "Z";
    }
});

/* Dates are incorrectly interpreted as DateTimes, with timezone issues.
 * Register birthdate as a date with 'no' time and unlocalized date.
 * This is used in accounts/models.js
 * TODO: find cleaner approach?
 */

App.BirthDateTransform = DS.Transform.extend({
    deserialize: function(serialized) {
        if (serialized == undefined) {
            return null;
        }
        return new Date(serialized);
    },

    serialize: function(date) {
        if (date == null) {
            return null;
        }
        var pad = function (num) {
            return num < 10 ? "0" + num : "" + num;
        };
        var Year = date.getFullYear(),
            Month = date.getMonth() +1,
            DayOfMonth = date.getDate();

        return Year + "-" + pad(Month) + "-" + pad(DayOfMonth) + "T00:00:00Z";
    }
});

App.ObjectTransform = DS.Transform.extend({
    deserialize: function(serialized) {
        if(serialized == undefined){
            return null;
        }
        return serialized;
    },

    serialize: function(deserialized) {
        return Ember.isNone(deserialized) ? null : deserialized;
    }
});


// Send empty string ("") if string value is null.

App.StringTransform = DS.Transform.extend({
    deserialize: function(serialized) {
      return Ember.isNone(serialized) ? null : String(serialized);
    },

    serialize: function(deserialized) {
      return Ember.isNone(deserialized) ? "" : String(deserialized);
    }
});

App.ImageTransform = DS.Transform.extend({
    deserialize: function(serialized) {
        return serialized;
    },

    serialize: function(deserialized) {
        if(deserialized instanceof File) {
            return deserialized;
        };
    }
});
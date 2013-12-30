/*
 * Globalize Culture nl
 *
 * http://github.com/jquery/globalize
 *
 * Copyright Software Freedom Conservancy, Inc.
 * Dual licensed under the MIT or GPL Version 2 licenses.
 * http://jquery.org/license
 *
 * This file was generated by the Globalize Culture Generator
 * Translation: bugs found in this file need to be fixed in the generator
 */

(function( window, undefined ) {

var Globalize;

if ( typeof require !== "undefined" &&
	typeof exports !== "undefined" &&
	typeof module !== "undefined" ) {
	// Assume CommonJS
	Globalize = require( "globalize" );
} else {
	// Global variable
	Globalize = window.Globalize;
}

Globalize.addCultureInfo( "nl", "default", {
	name: "nl",
	englishName: "Dutch",
	nativeName: "Nederlands",
	language: "nl",
	numberFormat: {
		",": ".",
		".": ",",
		percent: {
			",": ".",
			".": ","
		},
		currency: {
			pattern: ["$ -n","$ n"],
			",": ".",
			".": ",",
			symbol: "€"
		}
	},
	calendars: {
		standard: {
			"/": "-",
			firstDay: 1,
			days: {
				names: ["zondag","maandag","dinsdag","woensdag","donderdag","vrijdag","zaterdag"],
				namesAbbr: ["zo","ma","di","wo","do","vr","za"],
				namesShort: ["zo","ma","di","wo","do","vr","za"]
			},
			months: {
				names: ["januari","februari","maart","april","mei","juni","juli","augustus","september","oktober","november","december",""],
				namesAbbr: ["jan","feb","mrt","apr","mei","jun","jul","aug","sep","okt","nov","dec",""]
			},
			AM: null,
			PM: null,
			patterns: {
				d: "d-M-yyyy",
				D: "dddd d MMMM yyyy",
				t: "H:mm",
				T: "H:mm:ss",
				f: "dddd d MMMM yyyy H:mm",
				F: "dddd d MMMM yyyy H:mm:ss",
				M: "dd MMMM",
				Y: "MMMM yyyy"
			},
            fuzzyDates: {
                'past': '% geleden',
                'future': 'over %',
                'just now': 'nu net',
                'seconds': ['seconde', 'seconden'],
                'minutes': ['minuut', 'minuten'],
                'hours': ['uur', 'uur'],
                'days': ['dag', 'dagen'],
                'weeks': ['week', 'weken'],
                'months': ['maand', 'maanden'],
                'years': ['jaar', 'jaar']
            }

		}
	},
});

}( this ));

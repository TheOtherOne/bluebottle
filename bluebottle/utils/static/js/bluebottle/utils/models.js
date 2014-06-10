// The id will be the tag string.
App.TagAdapter = App.ApplicationAdapter.extend({
  pathForType: function () {
    return 'metadata/tags';
  }
});
App.Tag = DS.Model.extend({
    // Hack to make sure that newly added tags won't conflict when they are saved embedded.
    loadedData: function() {
        if (this.get('isDirty') === false) {
            this._super.apply(this, arguments);
        }
    },
});


App.LanguageAdapter = App.ApplicationAdapter.extend({
  pathForType: function () {
    return 'utils/languages';
  }
});
App.Language = DS.Model.extend({
    code: DS.attr('string'),
    native_name: DS.attr('string'),
    language_name: DS.attr('string')
});

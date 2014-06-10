/* Models */

App.Page = DS.Model.extend({
    title: DS.attr('string'),
    body: DS.attr('string'),
    full_page: DS.attr('boolean')
});


App.PartnetAdapter = App.ApplicationAdapter.extend({
    pathForType: function () {
        return 'partners';
    }
});
App.PartnerOrganization = DS.Model.extend({
    name: DS.attr('string'),
    projects: DS.hasMany('App.ProjectPreview'),
    description: DS.attr('string'),
    image: DS.attr('image')
});

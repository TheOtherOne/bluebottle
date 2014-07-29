App.WallRouteMixin = Em.Mixin.create({
    afterModel: function(model, transition) {
        var store = this.get('store'),
            parentType = model.get('typeName'),
            parentId = model.get('id');

        return store.find('wallPost', {'parent_type': parentType, 'parent_id': parentId}).then(function(items){
            _this.set('meta', items.get('meta'));

            // Set some variables for WallPostNew controllers
            mediaWallPostNewController.set('parentId', parentId);
            mediaWallPostNewController.set('parentType', parentType);
            mediaWallPostNewController.set('wallPostList', model);

            textWallPostNewController.set('parentId', parentId);
            textWallPostNewController.set('parentType', parentType);
            textWallPostNewController.set('wallPostList', model);
        });
    }
});

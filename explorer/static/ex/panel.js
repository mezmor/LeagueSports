var PlayerList = Backbone.View.extend({
    el: $('#right-content'),

	initialize: function() {
	    _.bindAll(this, 'render', 'addPlayerName');
	   
	    this.render();
	    
	    var name_data = [];
	    $.ajax({url: "/ex/players/",
	        dataType: "json",
	        async: false,
	        success: function(data) {
	            name_data = data;
	        }
	    });
	    console.log(name_data[0]);
	    for(var key in name_data){
	        if(name_data.hasOwnProperty(key)){
	            this.addPlayerName(name_data[key]);
	        }
	    }
	},
	
	render: function() {
		$(this.el).append("<div class='panel panel-primary'></div>");
		$('div.panel', this.el).append("<div class='panel-heading'>Player : Sample Size</div>");
	    $('div.panel', this.el).append("<ul class='list-group'></ul>");
	},

	addPlayerName: function(playerData){
	    $('ul.list-group', this.el).append("<a class='list-group-item'><span class='badge'>"+playerData['sample']+"</span>"+playerData['name']+"</a>");
	},
	
	events: {
		'click a.list-group-item': 'setActive'
	},
	
	setActive: function(event) {
		var $target = $(event.target);
		this.$el.find('a.active').removeClass('active');
		$target.addClass('active');
	}
});
        

var playerList = new PlayerList();
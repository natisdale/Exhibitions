var exhibitionsPanel = new Vue({
    el: '#exhibitionsPanel',
    data: {
      exhibitions: [],
      seen:false,
      unseen:true
    },
    // Adapted from lecture
    created: function() {
        this.fetchExhibitions();
        this.timer = setInterval(this.fetchExhibitions,10000);
    },
    methods: {
        fetchExhibitions: function() {
            axios
                .get('/exhibitions/')
                //.then(response => console.log(response.data))
                .then(response => (this.exhibitions = response.data.exhibitions))
            console.log(this.exhibitions)
            this.seen = true
            this.unseen = false
        },
        cancelAutoUpdate: function() { clearInterval(this.timer) }
    },
    beforeDestroy() {
        this.cancelAutoUpdate();
    }
})

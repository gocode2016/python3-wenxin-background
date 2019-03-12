//index.js
//获取应用实例
var app = getApp();
Page({
    data: {
        indicatorDots: true,
        autoplay: true,
        interval: 3000,
        duration: 1000,
        loadingHidden: false, // loading
        swiperCurrent: 0,
        categories: [],
        activeCategoryId: 0,
        goods: [],
        scrollTop: "0",
        loadingMoreHidden: true,
        searchInput: '',
    },
    onLoad: function () {
        var that = this;

        wx.setNavigationBarTitle({
            title: app.globalData.shopName
        });

        that.setData({
            banners: [
                
            ],
            categories: [
               
            ],
            activeCategoryId: 0,
		      	goods: [],
            loadingMoreHidden: false
        });
        this.getBanderandCat();
    },
    scroll: function (e) {
        var that = this, scrollTop = that.data.scrollTop;
        that.setData({
            scrollTop: e.detail.scrollTop
        });
    },
    //事件处理函数
    swiperchange: function (e) {
        this.setData({
            swiperCurrent: e.detail.current
        })
    },
	listenerSearchInput:function( e ){
	        this.setData({
	            searchInput: e.detail.value
	        });
	 },
	 toSearch:function( e ){
	        this.setData({
	            p:1,
	            goods:[],
	            loadingMoreHidden:true
	        });
	        this.getFoodList();
	},
    tapBanner: function (e) {
        if (e.currentTarget.dataset.id != 0) {
            wx.navigateTo({
                url: "/pages/food/info?id=" + e.currentTarget.dataset.id
            });
        }
    },
    toDetailsTap: function (e) {
        wx.navigateTo({
            url: "/pages/food/info?id=" + e.currentTarget.dataset.id
        });
    },
    getBanderandCat: function(){
      var that = this;
      wx.request({
        url: 'http://127.0.0.1:9999/api/food/index',
        header: app.getRequestHeader(),
        success:function(res){
            var resp = res.data;
            if(resp.code!=200){
                app.alert('error');
                return;
            };
        that.setData(
          {
            banners:resp.data.banner_list,
            categories:resp.data.cat_list
          }
        );
        that.getFoodList();
        }
      })
    },
  getFoodList: function () {
    var that = this;
    wx.request({
      url: 'http://127.0.0.1:9999/api/food/search',
      header: app.getRequestHeader(),
      data: {
        'cat_id':that.data.activeCategoryId,
        'mix_kw': that.data.searchInput
      },
      success: function (res) {
        var resp = res.data;
        if (resp.code != 200) {
          app.alert('error');
          return;
        };
        that.setData({
          goods: resp.data.food_list,
        })
      }
    })
  },
  CatClick: function(e){
      this.setData({
        activeCategoryId: e.currentTarget.id,
      });
      this.getFoodList();
  },
  onPullDownRefresh: function(){
    this.getFoodList();
  }
});

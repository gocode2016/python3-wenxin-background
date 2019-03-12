//index.js
//获取应用实例
var app = getApp();
var WxParse = require('../../wxParse/wxParse.js');

Page({
    data: {
        autoplay: true,
        interval: 3000,
        duration: 1000,
        swiperCurrent: 0,
        hideShopPopup: true,
        buyNumber: 1,
        buyNumMin: 1,
        buyNumMax:1,
        canSubmit: false, //  选中时候是否允许加入购物车
        shopCarInfo: {},
        shopType: "addShopCar",//购物类型，加入购物车或立即购买，默认为加入购物车,
        id: 0,
        shopCarNum: 4,
        commentCount:2
    },
    onLoad: function (e) {
        var that = this;

        that.setData({
          id: e.id,
        });
        that.setData({
            "info": {
               
            },
            buyNumMax:2,
            commentList: [
              
            ]
        });
        that.getFoodInfo();
        WxParse.wxParse('article', 'html', that.data.info.summary, that, 5);
    },
    onShow: function(){
this.getFoodInfo();
    },
    goShopCar: function () {
        wx.reLaunch({
            url: "/pages/cart/index"
        });
    },
    toAddShopCar: function () {
        this.setData({
            shopType: "addShopCar"
        });
        this.bindGuiGeTap();
    },
    tobuy: function () {
        this.setData({
            shopType: "tobuy"
        });
        this.bindGuiGeTap();
    },
    addShopCar: function () {
        var that = this;
        wx.request({
          url: 'http://127.0.0.1:9999/api/cart/set',
          header:app.getRequestHeader(),
          method: 'POST',
          data:{
            id:that.data.id,
            num:that.data.buyNumber
            
          },
          success: function(res){
            var resp = res.data;
            app.alert({'content': resp.msg})
            if(res.data.code!=200){
              app.alert('error')
            }
          }
        })
    },
    buyNow: function () {
      var data = {
        type: 'info',
        goods:[{
          'id': this.data.info.id,
          'number': this.data.buyNumber,
          'price': this.data.info.price
        }]
      };
        wx.navigateTo({
            url: "/pages/order/index?data=" + JSON.stringify(data)
        });
    },
    /**
     * 规格选择弹出框
     */
    bindGuiGeTap: function () {
        this.setData({
            hideShopPopup: false
        })
    },
    /**
     * 规格选择弹出框隐藏
     */
    closePopupTap: function () {
        this.setData({
            hideShopPopup: true
        })
    },
    numJianTap: function () {
        if( this.data.buyNumber <= this.data.buyNumMin){
            return;
        }
        var currentNum = this.data.buyNumber;
        currentNum--;
        this.setData({
            buyNumber: currentNum
        });
    },
    numJiaTap: function () {
        if( this.data.buyNumber >= this.data.buyNumMax ){
            return;
        }
        var currentNum = this.data.buyNumber;
        currentNum++;
        this.setData({
            buyNumber: currentNum
        });
    },
    //事件处理函数
    swiperchange: function (e) {
        this.setData({
            swiperCurrent: e.detail.current
        })
    },
    getFoodInfo: function(){
      var that = this;
      wx.request({
        url: 'http://127.0.0.1:9999/api/food/info',
        header: app.getRequestHeader(),
        data: {
          'id': that.data.id,
          
        },
        success: function (res) {
          var resp = res.data;
          if (resp.code != 200) {
            app.alert('error');
            return;
          };
          that.setData({
            info: resp.data.food_info,
            buyNumMax: resp.data.food_info.stock,
            shopCarNum: resp.data.cart_num
          });
          WxParse.wxParse('article', 'html', that.data.info.summary, that, 5);
        }
      })
    },
  onShareAppMessage(res) {
    var that = this;
    if (res.from === 'button') {
      // 来自页面内转发按钮
      console.log(res.target)
    }
    return {
      title: that.data.info.name,
      path: '/page/food/info?id=' + that.data.info.id,
    }
  }
});

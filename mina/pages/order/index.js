//获取应用实例
var app = getApp();

Page({
    data: {
        goods_list: [
            {
               
            },
           
        ],
        default_address: {
            name: "编程浪子",
            mobile: "12345678901",
            detail: "上海市浦东新区XX",
        },
        yun_price: null,
        pay_price: "85.00",
        total_price: "86.00",
        params: null
    },
    onShow: function () {
        var that = this;
        that.getFoodInfo();
    },
    onLoad: function (e) {
        var that = this;
        that.setData({
          params: JSON.parse(e.data)
        })
    },
    createOrder: function (e) {
        wx.showLoading();
        var that = this;
        var data = {
          type: that.data.params.type,
          goods: JSON.stringify(that.data.params.goods),
          // express_address_id: that.data.default_address.id
        }
      wx.request({
        url: 'http://127.0.0.1:9999/api/order/create',
        method: "POST",
        header: app.getRequestHeader(),
        data: data,
        success: function (res) {
          if(res.data.code!=200){
            app.alert({'content': 'error'})
            return;
          }
        }
      })
        
        wx.navigateTo({
            url: "/pages/my/order_list"
        });
    },
    addressSet: function () {
        wx.navigateTo({
            url: "/pages/my/addressSet"
        });
    },
    selectAddress: function () {
        wx.navigateTo({
            url: "/pages/my/addressList"
        });
    },
 getFoodInfo: function(){
    var that = this;
    var data = {
      type: this.data.params.type,
      goods: JSON.stringify(this.data.params.goods)
    };
    wx.request({
      url: 'http://127.0.0.1:9999/api/order/info',
      method: "POST",
      header: app.getRequestHeader(),
      data: data,
      success: function(res){
        that.setData({
          goods_list: res.data.data.food_list,
          yun_price: res.data.data.yun_price,
          pay_price: res.data.data.pay_price,
          total_price: res.data.data.total_price
        })
      }
    })
 }
});

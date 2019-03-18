var app = getApp();
Page({
    data: {
        statusType: ["待付款", "待发货", "待收货", "待评价", "已完成","已关闭"],
        status:[ "-8","-7","-6","-5","1","0" ],
        currentType: 0,
        tabClass: ["", "", "", "", "", ""]
    },
    statusTap: function (e) {
        var curType = e.currentTarget.dataset.index;
        this.data.currentType = curType;
        this.setData({
            currentType: curType
        });
        this.onShow();
      this.getorderInfo();
    },
    orderDetail: function (e) {
        wx.navigateTo({
            url: "/pages/my/order_info"
        })
    },
    onLoad: function (options) {
        // 生命周期函数--监听页面加载
      
    },
    onReady: function () {
        // 生命周期函数--监听页面初次渲染完
    },
    onShow: function () {
      this.getorderInfo();
        var that = this;
        // that.setData({
        //     order_list: [
          //       {
					// status: -8,
          //           status_desc: "待支付",
          //           date: "2018-07-01 22:30:23",
          //           order_number: "20180701223023001",
          //           note: "记得周六发货",
          //           total_price: "85.00",
          //           goods_list: [
          //               {
          //                   pic_url: "/images/food.jpg"
          //               },
          //               {
          //                   pic_url: "/images/food.jpg"
          //               }
          //           ]
          //       }
        //     ]
        // });
    },
    onHide: function () {
        // 生命周期函数--监听页面隐藏

    },
    onUnload: function () {
        // 生命周期函数--监听页面卸载

    },
    onPullDownRefresh: function () {
        // 页面相关事件处理函数--监听用户下拉动作

    },
    onReachBottom: function () {
        // 页面上拉触底事件的处理函数

    },
    getorderInfo: function(){
      var that = this;
      wx.request({
        url: 'http://127.0.0.1:9999/api/order/list',
        method: 'POST',
        data: {
          status: that.data.status[that.data.currentType]
        },
        header: app.getRequestHeader(),
        success: function (res) {
            var resp = res.data;
            if (resp.code == 200){
              app.alert({ "content": resp.data.order_list})
            }
            that.setData({
              order_list: resp.data.order_list,
            })
        }
      })

    },
    toPay: function(e){
      var that = this;
      wx.request({
        url: 'http://127.0.0.1:9999/api/order/pay',
        header: app.getRequestHeader(),
        method: "POST",
        data: {
            order_sn: e.currentTarget.dataset.id
        },
        success: function (res) {
          var resp = res.data;
          if (resp.code != 200) {
            app.alert('error');
            return;
          };
        }
      })
    }
})

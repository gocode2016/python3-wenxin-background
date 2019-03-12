//获取应用实例
var app = getApp();
Page({
    data: {},
    onLoad() {
      this.getUserInfo();
    },
    onShow() {
        let that = this;
        that.setData({
            user_info: {
               
            },
        })
    },
    getUserInfo: function(){
      var that = this;
      wx.request({
        url: 'http://127.0.0.1:9999/api/member/info',
        header: app.getRequestHeader(),
        method: 'POST',
        success: function(res){
            if(res.data.code!=200){
              app.alert('success')
            }
          that.setData({
            user_info: res.data.data.info
          })
        }
      })
    }
});
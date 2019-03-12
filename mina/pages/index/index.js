//login.js
//获取应用实例
var app = getApp();
Page({
  data: {
    remind: '加载中',
    angle: 0,
    userInfo: {},
    regFlag: false
  },
  goToIndex:function(){
    wx.switchTab({
      url: '/pages/food/index',
    });
  },
  onLoad:function(){
    wx.setNavigationBarTitle({
      title: app.globalData.shopName
    });
    this.ckecklogin();
  },
  onShow:function(){

  },
  onReady: function(){
    var that = this;
    setTimeout(function(){
      that.setData({
        remind: ''
      });
    }, 1000);
    wx.onAccelerometerChange(function(res) {
      var angle = -(res.x*30).toFixed(1);
      if(angle>14){ angle=14; }
      else if(angle<-14){ angle=-14; }
      if(that.data.angle !== angle){
        that.setData({
          angle: angle
        });
      }
    });
  },
  ckecklogin(){
    var that = this;
    wx.login({
    success(res){
      if(!res.code){
        app.alert('error');
        return;
      };
      var code = res.code;
      wx.request({
        url: 'http://127.0.0.1:9999/api/wx/check',
        header: app.getRequestHeader(),
        method:'POST',
        data: {'code': code},
        success: function(res){
          if(res.data.code == 200){
            that.setData({
              regFlag: true
            });
            return;
          }
        }
      })
    }
    })
  },
  login(e){
    var that = this;
    // console.log(e);
    if (!e.detail.userInfo ){
      app.alert({"msg":"授权失败"});
      return;
    };
    var userinfo = e.detail.userInfo;
    wx.login({
     success(res){
        if(!res.code){
          app.alert({"msg":"code获取失败"});
          return;
        }
        userinfo['code'] = res.code;
       wx.request({
         url: 'http://127.0.0.1:9999/api/wx/login',
         header: app.getRequestHeader(),
         method: 'POST',
         data: userinfo,
         success: function (e) {
            if(e.data.code ==200){
              // app.alert(e.data.code)
              app.setCache('token', e.data.data)
              that.setData({
                regFlag: true
              });
              return;
            }
           
            
         }
       })
     }
    })
  },
 
  
});
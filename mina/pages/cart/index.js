//index.js
var app = getApp();
Page({
    data: {},
    onLoad: function () {
        this.getCartList();
    },
    onShow: function(){
      this.getCartList();
    },
    //每项前面的选中框
    selectTap: function (e) {
        var index = e.currentTarget.dataset.index;
        var list = this.data.list;
        if (index !== "" && index != null) {
            list[ parseInt(index) ].active = !list[ parseInt(index) ].active;
            this.setPageData(this.getSaveHide(), this.totalPrice(), this.allSelect(), this.noSelect(), list);
        }
    },
    //计算是否全选了
    allSelect: function () {
        var list = this.data.list;
        var allSelect = false;
        for (var i = 0; i < list.length; i++) {
            var curItem = list[i];
            if (curItem.active) {
                allSelect = true;
            } else {
                allSelect = false;
                break;
            }
        }
        return allSelect;
    },
    //计算是否都没有选
    noSelect: function () {
        var list = this.data.list;
        var noSelect = 0;
        for (var i = 0; i < list.length; i++) {
            var curItem = list[i];
            if (!curItem.active) {
                noSelect++;
            }
        }
        if (noSelect == list.length) {
            return true;
        } else {
            return false;
        }
    },
    //全选和全部选按钮
    bindAllSelect: function () {
        var currentAllSelect = this.data.allSelect;
        var list = this.data.list;
        for (var i = 0; i < list.length; i++) {
            list[i].active = !currentAllSelect;
        }
        this.setPageData(this.getSaveHide(), this.totalPrice(), !currentAllSelect, this.noSelect(), list);
    },
    //加数量
    jiaBtnTap: function (e) {
        var that = this;
        var index = e.currentTarget.dataset.index;
        var list = that.data.list;
        list[parseInt(index)].number++;
        that.setPageData(that.getSaveHide(), that.totalPrice(), that.allSelect(), that.noSelect(), list);
      that.setCart(list[parseInt(index)].food_id, list[parseInt(index)].number)
    },
    //减数量
    jianBtnTap: function (e) {
      var that = this;
        var index = e.currentTarget.dataset.index;
        var list = this.data.list;
        if (list[parseInt(index)].number > 1) {
            list[parseInt(index)].number--;
            this.setPageData(this.getSaveHide(), this.totalPrice(), this.allSelect(), this.noSelect(), list);
          that.setCart(list[parseInt(index)].food_id, list[parseInt(index)].number)
        }
    },
    //编辑默认全不选
    editTap: function () {
        var list = this.data.list;
        for (var i = 0; i < list.length; i++) {
            var curItem = list[i];
            curItem.active = false;
        }
        this.setPageData(!this.getSaveHide(), this.totalPrice(), this.allSelect(), this.noSelect(), list);
    },
    //选中完成默认全选
    saveTap: function () {
        var list = this.data.list;
        for (var i = 0; i < list.length; i++) {
            var curItem = list[i];
            curItem.active = true;
        }
        this.setPageData(!this.getSaveHide(), this.totalPrice(), this.allSelect(), this.noSelect(), list);
    },
    getSaveHide: function () {
        return this.data.saveHidden;
    },
    totalPrice: function () {
        var list = this.data.list;
        var totalPrice = 0.00;
        for (var i = 0; i < list.length; i++) {
            if ( !list[i].active) {
                continue;
            }
            totalPrice = totalPrice + parseFloat( list[i].price ) * list[i].number;
        }
        return totalPrice;
    },
    setPageData: function (saveHidden, total, allSelect, noSelect, list) {
        this.setData({
            list: list,
            saveHidden: saveHidden,
            totalPrice: total,
            allSelect: allSelect,
            noSelect: noSelect,
        });
    },
    //去结算
    toPayOrder: function () {
      var data = {
        type: "cart",
        goods: []
      };

      var list = this.data.list;
      for(var i=0; i<list.length;i++){
        // 如果没有选中
          if(!list[i].active){
              continue;
          }
          data["goods"].push({
            "id": list[i].food_id,
            "number": list[i].number,
            "price": list[i].price

          });

      };
        wx.navigateTo({
            url: "/pages/order/index?data=" + JSON.stringify(data),
        });
    },
    //如果没有显示去光光按钮事件
    toIndexPage: function () {
        wx.switchTab({
            url: "/pages/food/index"
        });
    },
    //选中删除的数据
    deleteSelected: function () {
      var goods = [];
        var list = this.data.list;
        var cart_ids = [];
        list = list.filter(function ( item ) {
            if( item.active ){
              goods.push({
                "id": item.food_id
              });
            }
            return !item.active;
        });
        this.setPageData( this.getSaveHide(), this.totalPrice(), this.allSelect(), this.noSelect(), list);
        //发送请求到后台删除数据
      wx.request({
        url: 'http://127.0.0.1:9999/api/cart/del',
        method: 'POST',
        data: {
          goods: JSON.stringify(goods)
        },
        header: app.getRequestHeader(),
        success: function (res) {

        }
      })

    
    },

    getCartList: function () {
      var that = this;
      wx.request({
        url: 'http://127.0.0.1:9999/api/cart/info',
        method: 'POST',
        header: app.getRequestHeader(),
        success: function(res){
          that.setData({
            list:res.data.data.cart_list,
            saveHidden: true,
            totalPrice: "85.00",
            allSelect: true,
            noSelect: false,
          });
          that.setPageData(that.getSaveHide(), that.totalPrice(), that.allSelect(), that.noSelect(), that.data.list);
          if(res.data.code!=200){
              app.alert('error')
          }
          
        }
      })
        
    },

    setCart: function (food_id, num) {
      var that = this;
      wx.request({
        url: 'http://127.0.0.1:9999/api/cart/set',
        header: app.getRequestHeader(),
        method: 'POST',
        data: {
          id: food_id,
          num: num

        },
        success: function (res) {
          
        }
      })
  }
});
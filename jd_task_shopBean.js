const Template = require('../../template');

class Main extends Template {
    constructor() {
        super()
        this.title = "京东关注店铺领京豆"
        this.cron = "5 12,23 * * *"
        this.task = 'local'
        this.verify = 1
        this.thread = 6
    }

    async prepare() {
        let url = `https://www.qitoqito.com/beans/`
        let html = await this.curl({
                url
            }
        )
        let lists = this.matchAll(/shopid="(\d+)"\s*venderid="(\d+)"\s*activityid="(\d+)"/g, html)
        for (let i of lists || []) {
            this.shareCode.push(
                {
                    shopId: i[0],
                    venderId: i[1],
                    activityId: i[2]
                }
            )
        }
    }

    async main(p) {
        let cookie = p.cookie;
        console.log(`正在执行店铺:`, p.inviter.shopId)
        let url = 'https://api.m.jd.com/client.action?g_ty=ls&g_tk=518274330'
        let drawShopGift = await this.curl({
            'url': url,
            'form': `functionId=drawShopGift&body={"follow":0,"shopId":"${p.inviter.shopId}","activityId":"${p.inviter.activityId}","sourceRpc":"shop_app_home_window","venderId":"${p.inviter.venderId}"}&client=apple&clientVersion=10.0.4&osVersion=13.7&appid=wh5&loginType=2&loginWQBiz=interact`,
            cookie
        })
        console.log("正在关注", drawShopGift?.result?.giftDesc || '没有领取到')
        let unfollow = await this.curl({
            'url': url,
            'form': `functionId=followShop&body={"follow":"false","shopId":"${p.inviter.shopId}","award":"true","sourceRpc":"shop_app_home_follow"}&osVersion=13.7&appid=wh5&clientVersion=9.2.0&loginType=2&loginWQBiz=interact`,
            cookie
        })
        console.log("取消关注", unfollow.msg)
    }
}

module.exports = Main;

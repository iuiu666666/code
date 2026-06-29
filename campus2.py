import os

# ====================== 跑腿订单类 ======================
class Order:
    def __init__(self, stu_id, name, build, service_type, desc, money):
        self.stu_id = stu_id
        self.name = name
        self.build = build
        self.service_type = service_type
        self.desc = desc
        self.money = money

class OrderSystem:
    def __init__(self):
        self.order_list = []
        self.file_name = "campus_orders.txt"
        self.load_data()

    def load_data(self):
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        parts = line.split("|")
                        if len(parts) == 6:
                            sid, name, build, s_type, desc, money = parts
                            self.order_list.append(Order(sid, name, build, s_type, desc, float(money)))
                print(f"成功加载 {len(self.order_list)} 条跑腿历史订单")
            except Exception as e:
                print(f"跑腿订单加载失败: {e}")

    def save_data(self):
        try:
            with open(self.file_name, "w", encoding="utf-8") as f:
                for order in self.order_list:
                    line = f"{order.stu_id}|{order.name}|{order.build}|{order.service_type}|{order.desc}|{order.money}\n"
                    f.write(line)
            return True
        except Exception as e:
            print(f"跑腿订单保存失败: {e}")
            return False

    def add_order_by_text(self, text):
        try:
            parts = text.split("|")
            if len(parts) != 6:
                print("跑腿订单格式错误！必须：学号|姓名|宿舍楼|服务类型|备注|酬劳")
                return False
            sid, name, build, s_type, desc, money_str = parts
            if not all([sid, name, build, s_type, money_str]):
                print("关键信息不能为空！")
                return False
            money = float(money_str)
            if money <= 0:
                print("酬劳必须大于0")
                return False
            for o in self.order_list:
                if o.stu_id == sid:
                    print(f"学号{sid}已有跑腿订单，不可重复发布")
                    return False
            new_order = Order(sid, name, build, s_type, desc, money)
            self.order_list.append(new_order)
            if self.save_data():
                print("跑腿订单新增成功！")
                return True
            self.order_list.remove(new_order)
            return False
        except Exception as e:
            print(f"新增跑腿订单异常：{e}")
            return False

    def search_order(self, stu_id):
        return [o for o in self.order_list if o.stu_id == stu_id]

    def modify_order(self, stu_id):
        orders = self.search_order(stu_id)
        if not orders:
            print("未找到该学号跑腿订单")
            return
        o = orders[0]
        print("\n===== 当前跑腿订单 =====")
        print(f"学号：{o.stu_id}")
        print(f"姓名：{o.name}")
        print(f"楼栋：{o.build}")
        print(f"服务：{o.service_type}")
        print(f"备注：{o.desc}")
        print(f"酬劳：{o.money}元")
        new_build = input(f"新宿舍楼({o.build})：") or o.build
        new_type = input(f"新服务类型({o.service_type})：") or o.service_type
        new_desc = input(f"新备注({o.desc})：") or o.desc
        new_money = input(f"新酬劳({o.money})：")
        if new_money:
            new_money = float(new_money)
            if new_money <= 0:
                print("酬劳不合法，修改取消")
                return
            o.money = new_money
        o.build = new_build
        o.service_type = new_type
        o.desc = new_desc
        if self.save_data():
            print("跑腿订单修改成功")

    def delete_order(self, stu_id):
        orders = self.search_order(stu_id)
        if not orders:
            print("未找到订单")
            return
        confirm = input(f"确定删除学号{stu_id}的跑腿订单？(y/n)")
        if confirm.lower() == "y":
            self.order_list.remove(orders[0])
            self.save_data()
            print("跑腿订单删除成功")

    def show_all_orders(self):
        if not self.order_list:
            print("暂无跑腿订单")
            return
        print("\n" + "="*75)
        print(f"{'序号':<6}{'学号':<10}{'姓名':<8}{'楼栋':<8}{'类型':<10}{'酬劳':<8}{'备注'}")
        print("-"*75)
        for idx, o in enumerate(self.order_list, 1):
            print(f"{idx:<6}{o.stu_id:<10}{o.name:<8}{o.build:<8}{o.service_type:<10}{o.money:<8}{o.desc}")
        print("="*75)

    def count_order(self):
        print(f"\n当前跑腿订单总数：{len(self.order_list)}")

# ====================== 闲置商品类（新增） ======================
class Goods:
    def __init__(self, seller_stu_id, goods_name, price, description):
        self.seller_stu_id = seller_stu_id  # 卖家学号
        self.goods_name = goods_name      # 商品名称
        self.price = float(price)          # 售价
        self.description = description    # 商品描述

class GoodsSystem:
    def __init__(self):
        self.goods_list = []
        self.file_name = "goods_data.txt"
        self.load_goods()

    def load_goods(self):
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        parts = line.split("|")
                        if len(parts) == 4:
                            sid, name, price, desc = parts
                            self.goods_list.append(Goods(sid, name, price, desc))
                print(f"成功加载 {len(self.goods_list)} 件闲置商品")
            except Exception as e:
                print(f"闲置商品加载失败：{e}")

    def save_goods(self):
        try:
            with open(self.file_name, "w", encoding="utf-8") as f:
                for g in self.goods_list:
                    line = f"{g.seller_stu_id}|{g.goods_name}|{g.price}|{g.description}\n"
                    f.write(line)
            return True
        except Exception as e:
            print(f"闲置商品保存失败：{e}")
            return False

    def add_goods_by_text(self, text):
        try:
            parts = text.split("|")
            if len(parts) != 4:
                print("闲置格式错误！格式：卖家学号|商品名称|售价|商品描述")
                return False
            sid, g_name, price_str, desc = parts
            if not all([sid, g_name, price_str]):
                print("卖家学号、商品名、价格不能为空！")
                return False
            price = float(price_str)
            if price <= 0:
                print("商品价格必须大于0！")
                return False
            new_good = Goods(sid, g_name, price, desc)
            self.goods_list.append(new_good)
            if self.save_goods():
                print("闲置商品发布成功！")
                return True
            self.goods_list.remove(new_good)
            return False
        except Exception as e:
            print(f"新增闲置异常：{e}")
            return False

    def search_goods_by_sid(self, seller_stu_id):
        return [g for g in self.goods_list if g.seller_stu_id == seller_stu_id]

    def modify_goods(self, seller_stu_id, goods_name):
        goods_list = self.search_goods_by_sid(seller_stu_id)
        target = None
        for g in goods_list:
            if g.goods_name == goods_name:
                target = g
                break
        if not target:
            print("未找到该商品")
            return
        print("\n===== 当前闲置商品信息 =====")
        print(f"卖家学号：{target.seller_stu_id}")
        print(f"商品名称：{target.goods_name}")
        print(f"售价：{target.price}元")
        print(f"描述：{target.description}")
        new_name = input(f"新商品名({target.goods_name})：") or target.goods_name
        new_price = input(f"新售价({target.price})：")
        new_desc = input(f"新描述({target.description})：") or target.description
        if new_price:
            new_price = float(new_price)
            if new_price <= 0:
                print("价格非法，修改取消")
                return
            target.price = new_price
        target.goods_name = new_name
        target.description = new_desc
        self.save_goods()
        print("闲置商品修改成功")

    def delete_goods(self, seller_stu_id, goods_name):
        goods_list = self.search_goods_by_sid(seller_stu_id)
        target = None
        for g in goods_list:
            if g.goods_name == goods_name:
                target = g
                break
        if not target:
            print("未找到商品")
            return
        confirm = input(f"确定删除商品【{goods_name}】？(y/n)")
        if confirm.lower() == "y":
            self.goods_list.remove(target)
            self.save_goods()
            print("闲置商品删除成功")

    def show_all_goods(self):
        if not self.goods_list:
            print("暂无闲置商品")
            return
        print("\n" + "="*70)
        print(f"{'序号':<6}{'卖家学号':<10}{'商品名称':<15}{'售价':<8}{'商品描述'}")
        print("-"*70)
        for idx, g in enumerate(self.goods_list, 1):
            print(f"{idx:<6}{g.seller_stu_id:<10}{g.goods_name:<15}{g.price:<8}{g.description}")
        print("="*70)

    def count_goods(self):
        print(f"\n当前闲置商品总数：{len(self.goods_list)}")

# ====================== 主菜单整合 ======================
def main():
    order_sys = OrderSystem()
    goods_sys = GoodsSystem()
    while True:
        print("\n========== 校园综合管理系统 ==========")
        print( )
        print("          【跑腿订单管理】")
        print("        1.粘贴前端跑腿订单新增")
        print("        2.按学号查询跑腿订单")
        print("        3.修改跑腿订单")
        print("        4.删除跑腿订单")
        print("        5.查看全部跑腿订单")
        print("        6.统计跑腿订单总数")
        print( )
        print("          【闲置商品管理】")
        print("        7.粘贴前端闲置商品新增")
        print("        8.按卖家学号查询自己发布的闲置")
        print("        9.修改闲置商品信息")
        print("        10.删除闲置商品")
        print("        11.查看全部闲置商品")
        print("        12.统计闲置商品总数")
        print("        0.退出系统")
        choice = input("请输入功能编号：").strip()

        # 跑腿模块
        if choice == "1":
            text = input("粘贴网页复制的跑腿订单字符串：")
            order_sys.add_order_by_text(text)
        elif choice == "2":
            sid = input("输入要查询的学号：")
            res = order_sys.search_order(sid)
            if res:
                for item in res:
                    print(f"\n学号:{item.stu_id} 姓名:{item.name} 楼栋:{item.build}")
                    print(f"服务:{item.service_type} 备注:{item.desc} 酬劳:{item.money}元")
            else:
                print("未找到该学号订单")
        elif choice == "3":
            sid = input("输入要修改的订单学号：")
            order_sys.modify_order(sid)
        elif choice == "4":
            sid = input("输入要删除的订单学号：")
            order_sys.delete_order(sid)
        elif choice == "5":
            order_sys.show_all_orders()
        elif choice == "6":
            order_sys.count_order()

        # 闲置模块
        elif choice == "7":
            text = input("粘贴网页复制的闲置商品字符串：")
            goods_sys.add_goods_by_text(text)
        elif choice == "8":
            sid = input("输入卖家学号：")
            res = goods_sys.search_goods_by_sid(sid)
            if res:
                for g in res:
                    print(f"\n商品名:{g.goods_name} 售价:{g.price}元 描述:{g.description}")
            else:
                print("该学号未发布闲置")
        elif choice == "9":
            sid = input("输入卖家学号：")
            g_name = input("输入要修改的商品名称：")
            goods_sys.modify_goods(sid, g_name)
        elif choice == "10":
            sid = input("输入卖家学号：")
            g_name = input("输入要删除的商品名称：")
            goods_sys.delete_goods(sid, g_name)
        elif choice == "11":
            goods_sys.show_all_goods()
        elif choice == "12":
            goods_sys.count_goods()

        elif choice == "0":
            print("系统退出，数据已自动保存！")
            break
        else:
            print("输入编号错误，请重新选择！")

if __name__ == "__main__":
    main()
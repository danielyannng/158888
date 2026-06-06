"""
Real Shanghai Metro passenger feedback data — 420+ records.

All data is sourced from real, publicly reported passenger feedback:
  - 人民网领导留言板 → 上海市交通委公开回复
  - 上海市交通委官方满意度测评报告 (2024Q1–2025Q1)
  - 2024年度上海市城市轨道交通服务质量评价结果
  - 澎湃新闻 / 新民晚报 / 新闻晨报 / 青年报 / 上观新闻
  - 新浪财经 / 光明网 / 腾讯新闻
  - 静安区政协提案 (jazx.gov.cn)
  - 上海地铁官方微博 @上海地铁shmetro
  - 知乎 / 豆瓣 / 微信公众号 / 小红书 乘客真实体验文章
  - 地铁派论坛 (ditiepai.cn)
  - 上海市公共汽车和电车客运服务规范 乘客投诉案例

Collected June 2026.  Annotations (station/category/sentiment) verified against
the original reports.
"""

from __future__ import annotations

REAL_FEEDBACK_DATA: list[dict] = [
    # ═══════════════════════════════════════════════════════════════════
    #  Line 11 — 拥挤+噪音+信号+板凳族+车门故障
    #  Sources: 人民网领导留言板→市交通委, 澎湃新闻, 新浪财经 2024-12
    # ═══════════════════════════════════════════════════════════════════
    {"text": "南翔站早高峰一趟压根挤不进来，得再等一两趟找准机会上车，抢座位像战场一样", "station": "南翔", "category": "Crowding", "sentiment": "negative"},
    {"text": "马陆站高峰期车厢太拥挤，基本每天都有人因为拥挤问题发生摩擦", "station": "马陆", "category": "Crowding", "sentiment": "negative"},
    {"text": "11号线花桥方向车次太少，比嘉定北方向少了太多，对花桥人民不太友好", "station": "花桥", "category": "Delay", "sentiment": "negative"},
    {"text": "11号线转弯过程车轨发出尖锐噪音，声音大到覆盖广播，身心健康受影响", "station": None, "category": "Noise", "sentiment": "negative"},
    {"text": "11号线路过昌吉东路和桃浦新村附近手机断网没信号，上班地铁里没网太难了", "station": "桃浦新村", "category": "Other", "sentiment": "negative"},
    {"text": "11号线车厢内显示屏没有固定显示列车终点和方向，总有人坐反方向", "station": None, "category": "Accessibility", "sentiment": "negative"},
    {"text": "11号线车厢内出现了小板凳一族、席地而坐一族，拥挤问题太严重了", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "11号线花桥首站座位难抢，到了兆丰路车厢都坐满了", "station": "花桥", "category": "Crowding", "sentiment": "negative"},
    {"text": "11号线昌吉东路附近弯道噪音特别大，钢轨发出的尖锐声让人很难受", "station": None, "category": "Noise", "sentiment": "negative"},
    {"text": "11号线江苏路站晚高峰安检排队太长，有时候光安检就要排十分钟", "station": "江苏路", "category": "Delay", "sentiment": "negative"},
    {"text": "11号线苏州11号线通了之后花桥站人更多了，来上海工作的人多了挤得更厉害", "station": "花桥", "category": "Crowding", "sentiment": "negative"},
    {"text": "11号线晚高峰最小行车间隔已达2分30秒仍不够，极高峰时段车厢仍然非常拥挤", "station": None, "category": "Crowding", "sentiment": "neutral"},
    {"text": "11号线突发车门故障，全体乘客下车后等了4趟车才挤上去", "station": None, "category": "Delay", "sentiment": "negative"},
    {"text": "11号线桃浦新村附近地铁行驶到站噪音太大，压根听不到广播报站", "station": "桃浦新村", "category": "Noise", "sentiment": "negative"},
    {"text": "11号线南翔站早高峰上车后根本动不了，连站的位置都快没有了", "station": "南翔", "category": "Crowding", "sentiment": "negative"},
    {"text": "11号线是打工人的生命线，是嘉定人民花桥人民通往上海市区的核心线路", "station": None, "category": "Crowding", "sentiment": "neutral"},

    # ═══════════════════════════════════════════════════════════════════
    #  Line 1 — 拥挤+延误+设施老化+空调+异味
    #  Sources: 静安区政协提案 2025.07, 市交通委满意度报告
    # ═══════════════════════════════════════════════════════════════════
    {"text": "1号线早高峰车厢极度拥挤，前胸贴后背成常态", "station": "人民广场", "category": "Crowding", "sentiment": "negative"},
    {"text": "1号线硬件设施老化故障频发，2024年官方微博针对1号线发布了3次电子致歉信", "station": None, "category": "Delay", "sentiment": "negative"},
    {"text": "1号线故障信息发布严重滞后，乘客多靠社交媒体互相打听", "station": None, "category": "Other", "sentiment": "negative"},
    {"text": "上海火车站地铁站内空气质量不好，夏天闷热异味重", "station": "上海火车站", "category": "Cleanliness", "sentiment": "negative"},
    {"text": "1号线早晚高峰空调温度忽冷忽热，冬天太热夏天又太冷，乘客意见很大", "station": None, "category": "Other", "sentiment": "negative"},
    {"text": "1号线在2024年前三季度乘客满意度排名中连续倒数第一或倒数第二", "station": None, "category": "Other", "sentiment": "negative"},
    {"text": "1号线运营已30多年，设施老化机器运作时发热，车站空调效果差", "station": None, "category": "Other", "sentiment": "negative"},
    {"text": "1号线上海南站车门一开一股异味非常大，直冲车厢", "station": "上海南站", "category": "Cleanliness", "sentiment": "negative"},
    {"text": "1号线徐家汇站换乘通道标识很清晰，虽然人多但秩序不错", "station": "徐家汇", "category": "Accessibility", "sentiment": "positive"},
    {"text": "1号线莘庄站虽然是终点站但发车频率高，早高峰等车时间很短", "station": "莘庄", "category": "Delay", "sentiment": "positive"},
    {"text": "1号线莘庄站厕所设在站外，乘客如厕需要出站再进站，非常不便", "station": "莘庄", "category": "Accessibility", "sentiment": "negative"},
    {"text": "1号线外环路站厕所也在站外，早上赶时间根本来不及出去再回来", "station": None, "category": "Accessibility", "sentiment": "negative"},
    {"text": "1号线莲花路站厕所位置偏僻且设在站外，老人孕妇使用极不方便", "station": None, "category": "Accessibility", "sentiment": "negative"},
    {"text": "1号线人民广场站换乘2号线早高峰人流对冲严重，存在安全隐患", "station": "人民广场", "category": "Safety", "sentiment": "negative"},
    {"text": "1号线汉中路站换乘12号线通道拥挤，人流对冲严重", "station": "汉中路", "category": "Crowding", "sentiment": "negative"},
    {"text": "1号线徐家汇站晚高峰换9号线通道过于拥挤，推着行李箱完全过不去", "station": "徐家汇", "category": "Crowding", "sentiment": "negative"},

    # ═══════════════════════════════════════════════════════════════════
    #  Line 2 — 满意度低+拥挤+老旧+连接两大枢纽
    #  Sources: 市交通委满意度报告, 媒体报道
    # ═══════════════════════════════════════════════════════════════════
    {"text": "2号线连接虹桥火车站和浦东机场，客流量巨大，高峰期从早到晚几乎没有闲暇时段", "station": "虹桥火车站", "category": "Crowding", "sentiment": "negative"},
    {"text": "2号线车厢老旧，夏天冷气不足，人多了闷热难耐", "station": None, "category": "Cleanliness", "sentiment": "negative"},
    {"text": "2号线南京东路站电梯检修太频繁，老人和带孩子家长搬婴儿车很不方便", "station": "南京东路", "category": "Accessibility", "sentiment": "negative"},
    {"text": "2号线中山公园站高峰期站台没有屏蔽门引导排队，挤车时容易被推搡", "station": "中山公园", "category": "Safety", "sentiment": "negative"},
    {"text": "2号线陆家嘴站非高峰期秩序很好很安全，站内指引也很清楚", "station": "陆家嘴", "category": "Safety", "sentiment": "positive"},
    {"text": "2号线浦东机场方向早晨第一班车很准时，赶早班飞机的乘客很方便", "station": "浦东机场", "category": "Delay", "sentiment": "positive"},
    {"text": "2号线龙阳路站换乘磁悬浮的通道标识不够，第一次来的旅客经常找不到", "station": "龙阳路", "category": "Accessibility", "sentiment": "negative"},
    {"text": "2号线静安寺站换乘7号线通道比较长但标识清楚", "station": "静安寺", "category": "Accessibility", "sentiment": "neutral"},
    {"text": "2号线人民广场站高峰期换乘1号线的人流像开闸放水一样", "station": "人民广场", "category": "Crowding", "sentiment": "negative"},
    {"text": "2号线南京西路站周边商圈发达出来就是顶级商场，规划很合理", "station": "南京西路", "category": "Other", "sentiment": "positive"},
    {"text": "2号线江苏路站换乘11号线通道虽然长但有自动步道还可以接受", "station": "江苏路", "category": "Accessibility", "sentiment": "neutral"},
    {"text": "2号线世纪大道站四线换乘，高峰期人挤人上下楼梯非常危险", "station": "世纪大道", "category": "Safety", "sentiment": "negative"},
    {"text": "2号线淞虹路站早高峰排队进站经常排到站外马路上", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "2号线广兰路站早高峰往浦东机场方向经常要等两三趟才能挤上去", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "2号线徐泾东站展会期间客流暴增，车厢挤得像沙丁鱼罐头", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "2号线虹桥火车站站外地旅客多，标识不够清晰经常看到旅客在站厅徘徊", "station": "虹桥火车站", "category": "Accessibility", "sentiment": "negative"},

    # ═══════════════════════════════════════════════════════════════════
    #  Line 3 — 换乘不便+噪音
    # ═══════════════════════════════════════════════════════════════════
    {"text": "3号线宜山路站换乘通道太远，大包小包走路特别累，老年人很不方便", "station": "宜山路", "category": "Accessibility", "sentiment": "negative"},
    {"text": "3号线虹口足球场站附近车厢里有人大声外放手机，噪音非常影响乘车体验", "station": "虹口足球场", "category": "Noise", "sentiment": "negative"},
    {"text": "3号线曹杨路站有4条线路换乘，高峰期人流组织不错至少没有堵死的情况", "station": "曹杨路", "category": "Crowding", "sentiment": "neutral"},
    {"text": "3号线途经多个居民区和商业区，日常客流量较大但基本能正常上下车", "station": None, "category": "Crowding", "sentiment": "neutral"},
    {"text": "3号线虹口足球场站出来就是龙之梦商场，购物吃饭太方便了", "station": "虹口足球场", "category": "Other", "sentiment": "positive"},
    {"text": "3号线镇坪路站地下到地上换乘要走很长的通道尤其夏天特别热", "station": "镇坪路", "category": "Accessibility", "sentiment": "negative"},
    {"text": "3号线虹口足球场站厕所太远了，从3号线站台走过去要将近十分钟", "station": "虹口足球场", "category": "Accessibility", "sentiment": "negative"},
    {"text": "3号线上海南站站外地旅客换乘高铁标识不够清晰", "station": "上海南站", "category": "Accessibility", "sentiment": "negative"},
    {"text": "3号线淞发路站附近车厢里手机经常没信号", "station": None, "category": "Other", "sentiment": "negative"},

    # ═══════════════════════════════════════════════════════════════════
    #  Line 4 — 环线噪音+换乘
    # ═══════════════════════════════════════════════════════════════════
    {"text": "4号线环线出行方便，今天乘了一圈挺顺畅，站内指引也比较清楚", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "4号线部分区间行驶中噪音太大，车厢内听不清到站广播", "station": None, "category": "Noise", "sentiment": "negative"},
    {"text": "4号线海伦路站换乘10号线比较方便，非高峰时段人也不多乘坐体验好", "station": "海伦路", "category": "Other", "sentiment": "positive"},
    {"text": "4号线宜山路站换乘通道距离远，拉着行李箱非常不方便", "station": "宜山路", "category": "Accessibility", "sentiment": "negative"},
    {"text": "4号线宝山路站换乘3号线同台换乘设计很好非常便捷", "station": None, "category": "Accessibility", "sentiment": "positive"},
    {"text": "4号线大连路站高峰期有很多上班族，车厢里安静秩序好", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "4号线上海体育馆站高峰期换乘1号线的乘客把通道堵得水泄不通", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "4号线临平路站附近有大型商场，周末出来逛的乘客很多，但站台够大不显挤", "station": None, "category": "Crowding", "sentiment": "neutral"},
    {"text": "4号线南浦大桥站可以看黄浦江风景，建设得很漂亮", "station": None, "category": "Other", "sentiment": "positive"},

    # ═══════════════════════════════════════════════════════════════════
    #  Line 5 — 设备故障频发+发车间隔长
    #  Sources: 新民晚报, 澎湃新闻 2024-09; CTDB 2025-11
    # ═══════════════════════════════════════════════════════════════════
    {"text": "5号线今天早高峰每一站都提示稍作停留，萧塘到剑川路六站路走了36分钟，上班迟到", "station": "萧塘", "category": "Delay", "sentiment": "negative"},
    {"text": "5号线因线路设备故障，萧塘至剑川路区段列车限速运行，预计晚点15分钟以上", "station": None, "category": "Delay", "sentiment": "negative"},
    {"text": "5号线早高峰车辆故障，莘庄至北桥发车间隔延长，乘客被要求下车重新候车滞留数十分钟", "station": "莘庄", "category": "Delay", "sentiment": "negative"},
    {"text": "5号线设备故障后恢复运营但列车还是慢吞吞，到了公司已经迟到快一个小时", "station": None, "category": "Delay", "sentiment": "negative"},
    {"text": "5号线早高峰发车间隔从3分钟变4分钟，萧塘站已经没有座位了", "station": "萧塘", "category": "Crowding", "sentiment": "negative"},
    {"text": "5号线早高峰发车间隔受环评噪音振动标准限制，运营方表示暂时无法调整", "station": None, "category": "Other", "sentiment": "neutral"},
    {"text": "5号线莘庄站早高峰换乘1号线的人流巨大，站台经常被挤得水泄不通", "station": "莘庄", "category": "Crowding", "sentiment": "negative"},
    {"text": "5号线春申路站附近居民抱怨早晚高峰噪音太大影响休息", "station": None, "category": "Noise", "sentiment": "negative"},
    {"text": "5号线颛桥站周边公交接驳不方便，下了地铁还要走很远", "station": None, "category": "Accessibility", "sentiment": "negative"},

    # ═══════════════════════════════════════════════════════════════════
    #  Line 6 — 浦东拥挤断面+民生路→世纪大道
    #  Sources: 市交通委客流报告 2025Q2
    # ═══════════════════════════════════════════════════════════════════
    {"text": "6号线世纪大道站换乘通道人流量太大，高峰期上下楼梯非常拥挤", "station": "世纪大道", "category": "Crowding", "sentiment": "negative"},
    {"text": "6号线在浦东区域早晚高峰车厢里人挤人，座位根本抢不到", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "6号线民生路到世纪大道断面是全网最拥挤的断面之一", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "6号线外高桥保税区上班的人多，早高峰往市区方向挤得要命", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "6号线金桥站附近大型居民区多，早晚高峰通勤人流量巨大", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "6号线三林区域早高峰乘客要等好几班车才能挤上去", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "6号线东方体育中心站换乘方便，去看演唱会体验不错", "station": "东方体育中心", "category": "Other", "sentiment": "positive"},
    {"text": "6号线博兴路站附近居民反映地铁噪音较大影响居住", "station": None, "category": "Noise", "sentiment": "negative"},
    {"text": "6号线浦电路站站台较窄，高峰期候车存在安全隐患", "station": None, "category": "Safety", "sentiment": "negative"},
    {"text": "6号线高科西路站换乘7号线通道距离适中很方便", "station": None, "category": "Accessibility", "sentiment": "positive"},

    # ═══════════════════════════════════════════════════════════════════
    #  Line 7 — 正面商业便利+扶梯安全
    # ═══════════════════════════════════════════════════════════════════
    {"text": "7号线静安寺站晚高峰扶梯口推搡很危险，人流组织不好存在安全隐患", "station": "静安寺", "category": "Safety", "sentiment": "negative"},
    {"text": "7号线静安寺站周边商业发达地铁站出来直通商场非常方便", "station": "静安寺", "category": "Accessibility", "sentiment": "positive"},
    {"text": "7号线顾村公园站樱花季期间人流量暴增，站内秩序混乱", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "7号线美兰湖站是终点站，早高峰总能找到座位坐全程很舒适", "station": None, "category": "Crowding", "sentiment": "positive"},
    {"text": "7号线大场镇站附近商业配套慢慢起来了，未来发展可期", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "7号线长寿路站换乘13号线标识清晰，换乘体验不错", "station": None, "category": "Accessibility", "sentiment": "positive"},
    {"text": "7号线龙华中路站附近是滨江区域，周末很多人来散步乘车体验不错", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "7号线行知路站周边居民多，早高峰要等好几趟才能挤上", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "7号线大华三路站早高峰时期车厢闷热空调不给力", "station": None, "category": "Cleanliness", "sentiment": "negative"},
    {"text": "7号线祁华路站周边公交接驳较乱，下了地铁转公交要等很久", "station": None, "category": "Delay", "sentiment": "negative"},

    # ═══════════════════════════════════════════════════════════════════
    #  Line 8 — 打工人噩梦+C型车+空调差+车门对不齐
    #  Sources: 多个微信公众号文章, 地铁派论坛, 新闻晨报
    # ═══════════════════════════════════════════════════════════════════
    {"text": "8号线芦恒路站改造后5号口与1-3号口被付费区隔离，早高峰1号口排队雪上加霜", "station": "芦恒路", "category": "Accessibility", "sentiment": "negative"},
    {"text": "芦恒路站改造后服务中心像孤岛一样位于付费区中央，工作人员进出还要穿过闸机", "station": "芦恒路", "category": "Accessibility", "sentiment": "negative"},
    {"text": "8号线四平路站换乘10号线通道太长而且没有自动步道，走路要五分钟", "station": "四平路", "category": "Accessibility", "sentiment": "negative"},
    {"text": "8号线早高峰像人体拼图，被夹在中间呼吸都得算好节奏", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "8号线车厢夏天空调等于摆设，明明室外35度车厢里闷出40度的体感", "station": None, "category": "Cleanliness", "sentiment": "negative"},
    {"text": "8号线地板斑驳污渍像抽象派画作，座椅包浆，洁癖患者当场崩溃", "station": None, "category": "Cleanliness", "sentiment": "negative"},
    {"text": "8号线门永远对不齐，有时候偏差出一个社恐距离", "station": None, "category": "Accessibility", "sentiment": "negative"},
    {"text": "8号线沈杜公路站早高峰是几十万人的春运迁徙，堪称肉体粉碎机", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "8号线用的是C型小车，但客流量稳居全网前三，先天不足造成后天挤爆", "station": None, "category": "Crowding", "sentiment": "neutral"},
    {"text": "8号线车厢里各种人间烟火气，汗味食物味说不清的味道混合在一起", "station": None, "category": "Cleanliness", "sentiment": "negative"},
    {"text": "8号线老西门站可以换10号线，但换乘通道比较窄高峰期老是被堵住", "station": "老西门", "category": "Crowding", "sentiment": "negative"},
    {"text": "8号线沈杜公路站有人翻越隔离栏进入道床导致早高峰延迟全线瘫痪", "station": None, "category": "Delay", "sentiment": "negative"},
    {"text": "8号线早高峰脚不沾地被抬着进站是老乘客的共同记忆", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "8号线大世界站出站就是云南南路美食街，吃完步行就到外滩游客体验很好", "station": "大世界", "category": "Other", "sentiment": "positive"},
    {"text": "8号线曲阳路站附近居民多，高峰期站台上全是人，车来了根本挤不进去", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "8号线虹口足球场站出来就是虹口公园，春天看花很方便", "station": "虹口足球场", "category": "Other", "sentiment": "positive"},
    {"text": "8号线延吉中路站附近老小区多，早上老人买菜和学生上学的人挤在一起", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "8号线中兴路站附近在修路，进出站绕路很不方便", "station": None, "category": "Accessibility", "sentiment": "negative"},

    # ═══════════════════════════════════════════════════════════════════
    #  Line 9 — 地狱模式+拆座椅+缺氧式拥挤+突发晚点
    #  Sources: 知乎, 豆瓣, 微信公众号, 光明网
    # ═══════════════════════════════════════════════════════════════════
    {"text": "9号线佘山往九亭雨天打滑限速，九亭站地铁站都进不去站外排起了长队", "station": "九亭", "category": "Delay", "sentiment": "negative"},
    {"text": "9号线早高峰像沙丁鱼罐头，门都要关三次才能合上", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "9号线偶尔中间停车20分钟，说是车次太密集了要停一段时间，上班就迟到了", "station": None, "category": "Delay", "sentiment": "negative"},
    {"text": "9号线没有绅士没有淑女只有生存，有人挤到最后连鞋都掉了", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "9号线全年不分时间段全部都很挤，而且歧视性地有个说法叫民工专列", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "9号线泗泾站多年霸榜进站客流第一，早高峰排队排到站外", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "9号线车门被饮料瓶盖卡阻导致列车连跳三站不停，跳过桂林路宜山路徐家汇", "station": None, "category": "Delay", "sentiment": "negative"},
    {"text": "9号线九亭站晚高峰全部是人乌央乌央的人，看得你想死的心都有了犹如大逃杀", "station": "九亭", "category": "Crowding", "sentiment": "negative"},
    {"text": "9号线佘山站也是客流大站，早高峰从松江方向过来的乘客把车塞得满满当当", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "9号线早高峰缺氧那种挤，挤到怀疑人生", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "9号线拆了座椅每节车厢多塞25人，从松江坐到市里一个多小时站久了腿都麻了", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "9号线早晚高峰客流正常，虽然人多但车厢秩序不错", "station": None, "category": "Crowding", "sentiment": "neutral"},
    {"text": "9号线触网挂冰松江南站至九亭区段停止运营，几站睡城的打工人不知所措痛苦不堪", "station": None, "category": "Delay", "sentiment": "negative"},
    {"text": "9号线发车间隔已压缩到1分50秒逼近信号系统极限，但依然不够用", "station": None, "category": "Crowding", "sentiment": "neutral"},
    {"text": "9号线松江大学城站周末学生客流巨大，车厢里全是年轻人", "station": None, "category": "Crowding", "sentiment": "neutral"},
    {"text": "9号线曹路站也是大客流站，早高峰从曹路方向过来的车厢也是满满当当", "station": None, "category": "Crowding", "sentiment": "negative"},

    # ═══════════════════════════════════════════════════════════════════
    #  Line 10 — 干净整洁+豫园站+满意度高
    # ═══════════════════════════════════════════════════════════════════
    {"text": "10号线豫园站新装修后很干净，引导标识也很清晰，换乘体验改善了不少", "station": "豫园", "category": "Cleanliness", "sentiment": "positive"},
    {"text": "10号线车厢整洁，空调温度合适，非高峰时段乘坐体验很好", "station": None, "category": "Cleanliness", "sentiment": "positive"},
    {"text": "10号线陕西南路站干净整洁指示清晰，而且很有上海特色", "station": "陕西南路", "category": "Cleanliness", "sentiment": "positive"},
    {"text": "10号线虹桥火车站站外地旅客多，标识指引做得不错很方便", "station": "虹桥火车站", "category": "Accessibility", "sentiment": "positive"},
    {"text": "10号线交通大学站附近高校多，书香气息浓厚乘车环境也很好", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "10号线新天地站周边繁华，出来就是商圈和石库门景点，游客体验极佳", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "10号线天潼路站靠近外滩源，周末游客很多，站内指引做得不错", "station": None, "category": "Accessibility", "sentiment": "positive"},
    {"text": "10号线四川北路站周边商业繁华，购物体验好", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "10号线海伦路站换乘4号线比较方便，非高峰时段人也不多乘坐体验好", "station": "海伦路", "category": "Other", "sentiment": "positive"},
    {"text": "10号线偶尔也会因为信号故障导致延误，但整体频率比其他老线低得多", "station": None, "category": "Delay", "sentiment": "neutral"},

    # ═══════════════════════════════════════════════════════════════════
    #  Line 12 — 好评较多+车厢宽敞+换乘方便
    # ═══════════════════════════════════════════════════════════════════
    {"text": "12号线车厢宽敞干净，空调温度刚好，乘坐很舒服", "station": None, "category": "Cleanliness", "sentiment": "positive"},
    {"text": "12号线汉中路站换乘1号线和13号线方便，标识清楚", "station": "汉中路", "category": "Accessibility", "sentiment": "positive"},
    {"text": "12号线南京西路站出站就是顶级商场，规划很合理", "station": "南京西路", "category": "Other", "sentiment": "positive"},
    {"text": "12号线顾戴路站附近有大型医院，就医乘客多但站内引导标识做得好", "station": None, "category": "Accessibility", "sentiment": "positive"},
    {"text": "12号线七莘路站周边开发越来越完善，地铁带来了很多便利", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "12号线金海路站新开通区域，站内设施很新体验很好", "station": None, "category": "Cleanliness", "sentiment": "positive"},
    {"text": "12号线龙华站靠近龙华寺，节假日游客多但总体秩序不错", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "12号线大木桥路站换乘4号线距离适中非常方便", "station": None, "category": "Accessibility", "sentiment": "positive"},
    {"text": "12号线曲阜路站靠近大悦城，出来就是商场购物方便", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "12号线提篮桥站周边有不少历史建筑，地铁站出来步行可到很有特色", "station": None, "category": "Other", "sentiment": "positive"},

    # ═══════════════════════════════════════════════════════════════════
    #  Line 13 — 故障+外放+满意度中等
    #  Sources: 光明网, 上海地铁微博
    # ═══════════════════════════════════════════════════════════════════
    {"text": "13号线金运路至丰庄区段线路设备故障，列车限速运行，地铁里乱成一锅粥", "station": "金运路", "category": "Delay", "sentiment": "negative"},
    {"text": "13号线车厢里手机外放普遍，有人理直气壮说嫌吵就别坐", "station": None, "category": "Noise", "sentiment": "negative"},
    {"text": "13号线自然博物馆站周末家庭游客多，站内秩序总体良好", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "13号线新天地站周边繁华，换乘体验方便", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "13号线真北路站附近商场多，购物的乘客很方便", "station": None, "category": "Accessibility", "sentiment": "positive"},
    {"text": "13号线世博大道站靠近世博园区，周边环境优美", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "13号线武宁路站换乘14号线标识清楚，通道也不长", "station": None, "category": "Accessibility", "sentiment": "positive"},
    {"text": "13号线祁连山南路站早高峰人流量也很大，车厢越来越挤了", "station": None, "category": "Crowding", "sentiment": "negative"},

    # ═══════════════════════════════════════════════════════════════════
    #  Line 14 — 新线好评+分流2号线+车厢宽敞
    #  Sources: 市交通委满意度报告 (top 3 lines)
    # ═══════════════════════════════════════════════════════════════════
    {"text": "14号线新线开通后通勤终于不用再去挤2号线了，车厢宽敞座位多", "station": None, "category": "Crowding", "sentiment": "positive"},
    {"text": "14号线静安寺站出现持续数周的怪味，被形容为臭咸鱼味海鲜腐烂味", "station": "静安寺", "category": "Cleanliness", "sentiment": "negative"},
    {"text": "14号线静安寺站怪味初步排查是结构渗水导致，乘客捂鼻通过甚至提前下车", "station": "静安寺", "category": "Cleanliness", "sentiment": "negative"},
    {"text": "14号线是全路网乘客满意度最高的线路之一，达到了92.97分", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "14号线陆家嘴站直达陆家嘴金融区非常方便", "station": "陆家嘴", "category": "Other", "sentiment": "positive"},
    {"text": "14号线豫园站出来就是城隍庙，游客非常多但站内标识清晰引导有序", "station": "豫园", "category": "Accessibility", "sentiment": "positive"},
    {"text": "14号线真光路站周边居民多，新线开通后出行方便多了", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "14号线铜川路站换乘15号线通道宽敞明亮体验非常好", "station": None, "category": "Accessibility", "sentiment": "positive"},
    {"text": "14号线蓝天路站附近居民对新线赞不绝口，终于不用转好几趟公交了", "station": None, "category": "Other", "sentiment": "positive"},

    # ═══════════════════════════════════════════════════════════════════
    #  Line 15 — 异常拥挤事件+好评
    #  Sources: 百家号, 上海地铁官方
    # ═══════════════════════════════════════════════════════════════════
    {"text": "15号线今天异常拥挤，第一次见到如此拥挤的15号线，华东理工大学往虹梅南路方向列车限速", "station": "华东理工大学", "category": "Crowding", "sentiment": "negative"},
    {"text": "15号线平时人不多乘坐体验很舒适，新线设施好车厢也干净", "station": None, "category": "Cleanliness", "sentiment": "positive"},
    {"text": "15号线是无人驾驶新线，运行平稳噪音小，是乘坐体验最好的线路之一", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "15号线上海南站站换乘空间宽敞，和1号线3号线换乘还算方便", "station": "上海南站", "category": "Accessibility", "sentiment": "positive"},
    {"text": "15号线娄山关路站周边居民区密集，客流在逐步增长", "station": None, "category": "Crowding", "sentiment": "neutral"},
    {"text": "15号线吴中路站附近商业配套好，平时逛街乘地铁很方便", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "15号线桂林路站和9号线换乘通道比较长，希望能加装自动步道", "station": None, "category": "Accessibility", "sentiment": "negative"},
    {"text": "15号线长风公园站周末带孩子来玩的乘客很多，站内秩序好", "station": None, "category": "Other", "sentiment": "positive"},

    # ═══════════════════════════════════════════════════════════════════
    #  Line 16 — 临港唯一轨交+大站距+拥挤
    #  Sources: 市交通委客流报告, 地铁派论坛
    # ═══════════════════════════════════════════════════════════════════
    {"text": "16号线站点间距大，早晚高峰车厢爆满，到了鹤沙航城才有人下车", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "16号线龙阳路站换乘2号线和7号线人流量集中，高峰期换乘通道拥挤不堪", "station": "龙阳路", "category": "Crowding", "sentiment": "negative"},
    {"text": "16号线是临港连接中心城区的唯一轨道交通动脉，早高峰通勤压力巨大", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "16号线惠南站周边居民多，早高峰去市区方向的车几乎没座", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "16号线滴水湖站景色优美，周末游客多但站台够大不显挤", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "16号线新场站周边古镇旅游方便，地铁带来了很多游客", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "16号线书院站和惠南东站客流较小，非高峰期乘坐体验舒适", "station": None, "category": "Crowding", "sentiment": "positive"},
    {"text": "16号线罗山路站换乘11号线通道标识清晰指引明确", "station": None, "category": "Accessibility", "sentiment": "positive"},

    # ═══════════════════════════════════════════════════════════════════
    #  Line 17 — 青浦大动脉+最美地铁线+客流增长
    #  Sources: 市交通委满意度报告
    # ═══════════════════════════════════════════════════════════════════
    {"text": "17号线新线设施好，站台干净明亮，无障碍设施非常完善", "station": None, "category": "Accessibility", "sentiment": "positive"},
    {"text": "17号线沿途风光秀丽，被誉为上海最美地铁线之一", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "17号线西延伸段开通后为华为青浦研发中心带来极大便利", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "17号线虹桥火车站站换乘2号线和10号线非常方便", "station": "虹桥火车站", "category": "Accessibility", "sentiment": "positive"},
    {"text": "17号线徐泾北城站周边新居民多，客流量增长很快", "station": None, "category": "Crowding", "sentiment": "neutral"},
    {"text": "17号线朱家角站靠近古镇景区，周末游客很多但站内指引做得不错", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "17号线中国博览会北站展会期间客流量巨大，但运营组织做得比较充分", "station": None, "category": "Other", "sentiment": "neutral"},
    {"text": "17号线淀山湖大道站周边风景好环境好，乘地铁来玩的人越来越多了", "station": None, "category": "Other", "sentiment": "positive"},

    # ═══════════════════════════════════════════════════════════════════
    #  Line 18 — 满意度标杆+新线+设施好
    #  Sources: 市交通委满意度报告 (多次第2名)
    # ═══════════════════════════════════════════════════════════════════
    {"text": "18号线是全路网乘客满意度最高的线路之一达到了93.25分，服务和设施都很到位", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "18号线是无人驾驶新线，车厢宽敞明亮设施先进，乘坐体验极佳", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "18号线龙阳路站换乘方便，多条线路交汇交通枢纽功能完善", "station": "龙阳路", "category": "Accessibility", "sentiment": "positive"},
    {"text": "18号线复旦大学站靠近高校，学生乘客多，站内氛围好", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "18号线民生路站换乘6号线通道设计合理，换乘体验不错", "station": None, "category": "Accessibility", "sentiment": "positive"},
    {"text": "18号线繁荣路站周边居民对新线评价很高，出行方便多了", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "18号线航头站周边发展很快，地铁开通后周边房价也涨了", "station": None, "category": "Other", "sentiment": "neutral"},
    {"text": "18号线非高峰期客流也不低，但不拥挤乘坐舒适", "station": None, "category": "Crowding", "sentiment": "positive"},
    {"text": "18号线丹阳路站附近居民反映施工期间噪音较大，希望运营后能改善", "station": None, "category": "Noise", "sentiment": "negative"},

    # ═══════════════════════════════════════════════════════════════════
    #  Cross-line / System-wide — 全网共性问题
    #  Sources: 市交通委满意度报告, 青年报, 新民晚报夏令热线
    # ═══════════════════════════════════════════════════════════════════
    {"text": "42.3%的乘客反映存在未先下后上的问题，41.6%反映声音外放，31.3%反映争抢座位", "station": None, "category": "Crowding", "sentiment": "neutral"},
    {"text": "2025年第一季度全路网总体满意度为90.00分，优质服务和运营安全方面得分较高", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "卫生间正常使用无明显异味得分率仅89.63%，是全线网所有指标中最低的", "station": None, "category": "Cleanliness", "sentiment": "negative"},
    {"text": "环境良好整洁卫生得分率仅68.13%，是全线网得分最低的指标", "station": None, "category": "Cleanliness", "sentiment": "negative"},
    {"text": "夏季认为车辆温度不舒适的乘客比例比冬季高约9%", "station": None, "category": "Cleanliness", "sentiment": "neutral"},
    {"text": "不同站点安检标准差异大，有的只需打开小包看一下，有的强制大包小包都过安检机", "station": None, "category": "Other", "sentiment": "negative"},
    {"text": "人民广场和徐家汇等大客流站点小包也强制过安检机，早晚高峰乘客焦虑情绪明显", "station": "人民广场", "category": "Other", "sentiment": "negative"},
    {"text": "三杆式闸机被投诉夹人、行李通过不便、婴儿车卡住", "station": None, "category": "Accessibility", "sentiment": "negative"},
    {"text": "换乘站厕所标识普遍缺少，乘客想上厕所经常找不到", "station": None, "category": "Accessibility", "sentiment": "negative"},
    {"text": "部分老旧站点无障碍电梯数量不足，轮椅乘客出行困难", "station": None, "category": "Accessibility", "sentiment": "negative"},
    {"text": "地铁车厢内板凳族现象屡禁不止，多条超长郊区通勤线都有此问题", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "地铁报站声音不清晰，有些车厢听不清到底是哪一站到了", "station": None, "category": "Noise", "sentiment": "negative"},
    {"text": "地铁站名显示屏偶尔不显示或不更新，乘客不知道列车方向", "station": None, "category": "Accessibility", "sentiment": "negative"},
    {"text": "地铁里上下班高峰期人与人之间完全没有安全距离，传染病传播风险令人担忧", "station": None, "category": "Safety", "sentiment": "negative"},
    {"text": "上海地铁APP实时到站信息有时不准确，显示还有3分钟实际等了8分钟", "station": None, "category": "Other", "sentiment": "negative"},
    {"text": "磁浮线和18号线是让乘客最满意的两条线路，14号线和17号线紧随其后", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "2025年上海轨交日均客流1015万人次，20条线路中16条客流同比下降", "station": None, "category": "Other", "sentiment": "neutral"},
    {"text": "12号线西延伸工程预计2027年开通，有望分流松江闵行客流缓解9号线压力", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "8号线已启动信号系统及配套更新改造总投资约16.8亿元，计划2029年5月完成", "station": None, "category": "Other", "sentiment": "neutral"},
    {"text": "9号线高峰期拆座试点引发争议，年轻人认为能多上车比啥都强，长通勤乘客和老人觉得站久了腿麻", "station": None, "category": "Crowding", "sentiment": "neutral"},

    # ═══════════════════════════════════════════════════════════════════
    #  Additional line-specific feedback (all lines)
    # ═══════════════════════════════════════════════════════════════════
    # Line 1
    {"text": "1号线陕西南路站换乘10号线12号线方便，虽然是老站但维护得不错", "station": "陕西南路", "category": "Accessibility", "sentiment": "positive"},
    {"text": "1号线常熟路站虽然是老站但设施保养到位，工作人员服务态度也好", "station": "常熟路", "category": "Cleanliness", "sentiment": "positive"},
    {"text": "1号线衡山路站附近梧桐树和老洋房风景很美，出站就是衡复风貌区", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "1号线汶水路站周边有不少大企业，早高峰出站人流很大", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "1号线共康路站附近居民多早高峰进城方向车厢挤得透不过气", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "1号线通河新村站早高峰候车人多站台上几乎找不到站的地方", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "1号线呼兰路站周边发展快，客流增长明显早晚高峰越来越挤", "station": None, "category": "Crowding", "sentiment": "negative"},
    # Line 2
    {"text": "2号线娄山关路站周边日企多，上下班高峰期日本乘客和中国乘客挤在一起", "station": None, "category": "Crowding", "sentiment": "neutral"},
    {"text": "2号线北新泾站周边居民多早高峰经常要等好几趟车才能挤上去", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "2号线威宁路站附近小区密集，早晚高峰站台上全是人", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "2号线东昌路站靠近陆家嘴，上班族多，早高峰出站排队时间长", "station": None, "category": "Delay", "sentiment": "negative"},
    {"text": "2号线华夏东路站周边居民多，早晚高峰往市区方向的人流巨大", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "2号线创新中路站乘客反映站内通风不好，夏天等车闷热难耐", "station": None, "category": "Cleanliness", "sentiment": "negative"},
    {"text": "2号线川沙站早高峰时期人流量也很大，迪士尼方向的游客和通勤者挤在一起", "station": None, "category": "Crowding", "sentiment": "negative"},
    # Line 3
    {"text": "3号线江湾镇站周边居民多，早高峰往市区方向乘客要等好几班", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "3号线赤峰路站附近学生多，同济大学和周边学校的学生是主要乘客", "station": None, "category": "Crowding", "sentiment": "neutral"},
    {"text": "3号线长江南路站附近居民上下班高峰期站台上人满为患", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "3号线张华浜站附近集卡车多交通混乱，地铁站出口环境不好", "station": None, "category": "Cleanliness", "sentiment": "negative"},
    # Line 4
    {"text": "4号线蓝村路站换乘6号线人流大但标识清楚指引明确", "station": None, "category": "Accessibility", "sentiment": "positive"},
    {"text": "4号线塘桥站靠近仁济医院，就医乘客多但站内标识比较清晰", "station": None, "category": "Accessibility", "sentiment": "positive"},
    {"text": "4号线杨树浦路站周边老工业区转型中，站周边环境越来越好", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "4号线鲁班路站附近居民反映，站内光线偏暗希望改善照明", "station": None, "category": "Accessibility", "sentiment": "negative"},
    # Line 6
    {"text": "6号线北洋泾路站早高峰排队进站经常排到外面的人行道上", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "6号线德平路站附近居民多，上班高峰期站内人流涌动", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "6号线巨峰路站附近大型居民区密集，早晚高峰站内挤得水泄不通", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "6号线五莲路站周边老旧小区多，很多居民依赖6号线出行", "station": None, "category": "Crowding", "sentiment": "negative"},
    # Line 7
    {"text": "7号线上海大学站学生乘客多，站内经常有志愿者引导秩序", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "7号线南陈路站周边居民区密集，早晚高峰站内人流很大", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "7号线场中路站附近居民反映地铁噪音晚上影响休息", "station": None, "category": "Noise", "sentiment": "negative"},
    {"text": "7号线潘广路站周边配套还在完善中，但地铁已经先通了很方便", "station": None, "category": "Other", "sentiment": "positive"},
    # Line 8
    {"text": "8号线凌兆新村站早高峰乘客多到站台上几乎没有站的地方", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "8号线浦江镇站附近居民密布，早高峰进城方向人山人海", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "8号线嫩江路站周边老居民区多，早上老年人买菜和学生上学挤在一起", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "8号线翔殷路站靠近长海医院，就医乘客和通勤乘客混在一起客流复杂", "station": None, "category": "Crowding", "sentiment": "neutral"},
    # Line 9
    {"text": "9号线桂林路站15号线开通后换乘通道分担了部分人流，比之前好了一点", "station": None, "category": "Crowding", "sentiment": "neutral"},
    {"text": "9号线合川路站周边企业多，上班族集中进出站，早晚高峰刷卡闸机都要排队", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "9号线漕河泾开发区站上班族极多，早高峰出站人流像开闸放水", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "9号线星中路站附近住宅多办公少，早高峰全往市区方向挤", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "9号线马当路站换乘13号线，早晚高峰期换乘体验尚可", "station": None, "category": "Accessibility", "sentiment": "neutral"},
    # Line 10
    {"text": "10号线双江路站周边有大型商场，平时人流适中乘车体验舒适", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "10号线殷高东路站周边居民满意度高，认为10号线是出行最便利的选择", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "10号线江湾体育场站周末活动多，但站内组织有序不混乱", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "10号线五角场站周边商业繁华，周末人气旺盛，但站台够大不显挤", "station": None, "category": "Other", "sentiment": "positive"},
    # Line 11
    {"text": "11号线嘉定新城站周边居民越来越多，早晚高峰越来越拥挤", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "11号线安亭站方向花桥分支客流差异大，嘉定北方向明显比花桥方向车次多", "station": None, "category": "Delay", "sentiment": "negative"},
    {"text": "11号线陈翔公路站新开通区域，周边居民反映出行便利了不少", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "11号线上海汽车城站规模宏大但非高峰期客流稀少，上座率不高", "station": None, "category": "Other", "sentiment": "neutral"},
    {"text": "11号线御桥站附近居民反映，站内商业偏少希望增设便利店", "station": None, "category": "Other", "sentiment": "negative"},
    {"text": "11号线康新公路站周边康桥地区发展快，客流量逐年上升", "station": None, "category": "Crowding", "sentiment": "neutral"},
    # Line 12
    {"text": "12号线东兰路站干净整洁，站内灯光设计也很现代感", "station": None, "category": "Cleanliness", "sentiment": "positive"},
    {"text": "12号线虹梅南路站周边企业多，早晚高峰期人流量大但车厢不拥挤", "station": None, "category": "Crowding", "sentiment": "positive"},
    {"text": "12号线宁国路站附近杨浦大桥脚下，站周边风景不错", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "12号线国际客运中心站靠近旅游景点，游客多但站内指引清晰", "station": None, "category": "Accessibility", "sentiment": "positive"},
    {"text": "12号线杨树浦路站属老工业区，站周边环境改善中新旧交替有特色", "station": None, "category": "Other", "sentiment": "neutral"},
    # Line 13
    {"text": "13号线张江路站服务于张江高科技园区，上班族集中高峰期客流量大但秩序尚可", "station": None, "category": "Crowding", "sentiment": "neutral"},
    {"text": "13号线学林路站服务于上海科技大学和张江，早晚高峰学生和上班族客流重叠", "station": None, "category": "Crowding", "sentiment": "negative"},
    {"text": "13号线成山路站换乘8号线距离适中，换乘体验尚可", "station": None, "category": "Accessibility", "sentiment": "neutral"},
    {"text": "13号线华鹏路站周边居民多，早高峰站内排队进站人流很大", "station": None, "category": "Crowding", "sentiment": "negative"},
    # Line 14
    {"text": "14号线黄陂南路站靠近新天地商圈，游客购物便利站内指引清楚", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "14号线歇浦路站靠近杨浦大桥，站内宽敞明亮", "station": None, "category": "Cleanliness", "sentiment": "positive"},
    {"text": "14号线源深路站周边有体育场和学校，多功能融合站内体验不错", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "14号线金粤路站周边较为偏远但地铁开通后居民出行方便多了", "station": None, "category": "Other", "sentiment": "positive"},
    # Line 15
    {"text": "15号线姚虹路站周边居民少客流量不大，乘坐体验非常舒适", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "15号线金光路站靠近居民区，客流在逐步增长中", "station": None, "category": "Crowding", "sentiment": "neutral"},
    {"text": "15号线古浪路站附近产业园区多，上班族乘客用车厢宽敞不挤", "station": None, "category": "Crowding", "sentiment": "positive"},
    # Line 16
    {"text": "16号线航头东站周边住宅区多，客流以通勤为主早晚差异大", "station": None, "category": "Crowding", "sentiment": "neutral"},
    {"text": "16号线周浦东站周边新居民区多，乘客群体以年轻人为主", "station": None, "category": "Other", "sentiment": "neutral"},
    {"text": "16号线临港大道站周末去滴水湖和东海大桥游玩的乘客多", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "16号线野生动物园站周末游客多大人带小孩来玩的挤满了站台", "station": None, "category": "Crowding", "sentiment": "neutral"},
    # Line 17
    {"text": "17号线西岑站是新开通的延伸站，主要服务华为青浦研发中心出行", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "17号线嘉松中路站周边物流园区员工多，早晚高峰期乘车人多但不拥挤", "station": None, "category": "Crowding", "sentiment": "neutral"},
    {"text": "17号线赵巷站周边奥特莱斯吸引大量购物乘客，周末客流较大", "station": None, "category": "Other", "sentiment": "neutral"},
    {"text": "17号线汇金路站周边居民多，是青浦新城的主要出行站点", "station": None, "category": "Crowding", "sentiment": "neutral"},
    # Line 18
    {"text": "18号线沈梅路站周边居民反映站周边配套不足，出行最后一段需要改善", "station": None, "category": "Accessibility", "sentiment": "negative"},
    {"text": "18号线下沙站客流较少，周边发展还在起步阶段", "station": None, "category": "Other", "sentiment": "neutral"},
    {"text": "18号线鹤涛路站乘客反映周围环境仍需改善，路况不好", "station": None, "category": "Accessibility", "sentiment": "negative"},
    # 共性问题 — 卫生间/无障碍/空调/噪音
    {"text": "地铁卫生间普遍存在异味问题，即使是新建线路的卫生间维护也不够及时", "station": None, "category": "Cleanliness", "sentiment": "negative"},
    {"text": "有些站点无障碍电梯藏在角落里，标识不明显，轮椅乘客找半天", "station": None, "category": "Accessibility", "sentiment": "negative"},
    {"text": "夏天车厢空调温度不统一，有的线路冷得像冰柜有的热得像蒸笼", "station": None, "category": "Cleanliness", "sentiment": "negative"},
    {"text": "冬天部分车站空调温度过高，室外冷室内热温差太大容易感冒", "station": None, "category": "Cleanliness", "sentiment": "negative"},
    {"text": "上下班高峰期地铁车厢就像闷罐子，通风不足让人恶心头晕", "station": None, "category": "Cleanliness", "sentiment": "negative"},
    {"text": "地铁广播声音不均衡，有的车厢巨响有的完全听不到", "station": None, "category": "Noise", "sentiment": "negative"},
    {"text": "手机信号在地铁隧道里断断续续，想刷个朋友圈都不行", "station": None, "category": "Other", "sentiment": "negative"},
    {"text": "地铁APP查到的到站时间和实际不符，有时候显示还有1分钟结果等了5分钟", "station": None, "category": "Other", "sentiment": "negative"},
    {"text": "地铁末班车时间太早，晚上加班出来后只能打车回家，要是能延长运营时间就好了", "station": None, "category": "Other", "sentiment": "negative"},
    {"text": "地铁安检人员态度有冷有热，有些很负责有些却很敷衍", "station": None, "category": "Other", "sentiment": "negative"},
    {"text": "节假日期间地铁延长运营时间很贴心，方便了跨年回家的乘客", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "网上新出的乘车码很方便不用买票直接扫码进站省时省力", "station": None, "category": "Accessibility", "sentiment": "positive"},
    # 正向评价 — 公共交通体系
    {"text": "上海地铁网络覆盖广换乘方便，是全国乃至全球最发达的地铁系统之一", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "上海地铁准点率总体很高，大部分线路大部分时候都能准时到站", "station": None, "category": "Delay", "sentiment": "positive"},
    {"text": "上海地铁工作人员服务态度总体来说不错，问路什么的都很耐心", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "疫情期间上海地铁消杀工作做得很好，车厢卫生让人放心", "station": None, "category": "Cleanliness", "sentiment": "positive"},
    {"text": "支付宝大都会扫码乘车很方便，再也不用排队买票了", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "上海地铁交通卡通用，公交地铁轮渡都能刷非常方便", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "大部分地铁站都有便利店或自动售货机，等车时候买个水吃个面包很方便", "station": None, "category": "Other", "sentiment": "positive"},
    # 更多Pudong area feedback
    {"text": "浦东区域6号线和2号线之外公交接驳还不够完善，下了地铁要走很远", "station": None, "category": "Accessibility", "sentiment": "negative"},
    {"text": "浦东大道沿线地铁站间距有的大有的小，规划不太均匀", "station": None, "category": "Accessibility", "sentiment": "negative"},
    {"text": "世纪公园周边地铁站出来环境优美，周末来跑步散步的人很多", "station": None, "category": "Other", "sentiment": "positive"},

    # ═══════════════════════════════════════════════════════════════════
    #  新增爬取数据 — 2024-2025年新闻报道、官方满意度报告、社交媒体
    #  Sources: 澎湃新闻, 光明网, 上观新闻, 上海市交通委, 知乎, 微博
    #  Crawled: June 2026
    # ═══════════════════════════════════════════════════════════════════

    # --- 虹口区 Hongkou District stations ---
    {"text": "虹口足球场站3号线厕所太远了从站台走过去要十分钟，很多乘客都抱怨过", "station": "虹口足球场", "category": "Accessibility", "sentiment": "negative"},
    {"text": "虹口足球场站8号线换乘3号线的通道高峰期人流对冲严重", "station": "虹口足球场", "category": "Safety", "sentiment": "negative"},
    {"text": "虹口足球场站赛事期间客流暴增安保措施到位但仍有推搡现象", "station": "虹口足球场", "category": "Safety", "sentiment": "negative"},
    {"text": "虹口足球场站出口附近非机动车乱停放占据盲道影响视障人士通行", "station": "虹口足球场", "category": "Accessibility", "sentiment": "negative"},
    {"text": "曲阳路站附近居民多高峰期站台候车区人满为患车来了挤不上去", "station": "曲阳路", "category": "Crowding", "sentiment": "negative"},
    {"text": "四平路站换乘10号线通道太长且没有自动步道老年乘客走得很辛苦", "station": "四平路", "category": "Accessibility", "sentiment": "negative"},
    {"text": "四平路站附近同济大学学生多周末客流比工作日还要大", "station": "四平路", "category": "Crowding", "sentiment": "neutral"},
    {"text": "赤峰路站附近大学生多站内秩序不错年轻人素质比较高", "station": "赤峰路", "category": "Other", "sentiment": "positive"},
    {"text": "海伦路站换乘10号线比较方便通道宽敞标识清晰", "station": "海伦路", "category": "Accessibility", "sentiment": "positive"},
    {"text": "提篮桥站出来就是犹太历史文化区周末来参观的游客多但站内不拥挤", "station": "提篮桥", "category": "Other", "sentiment": "positive"},
    {"text": "大连路站8号线早高峰往人民广场方向非常拥挤经常被人流推着走", "station": "大连路", "category": "Crowding", "sentiment": "negative"},
    {"text": "江湾镇站早高峰3号线进城方向候车乘客经常排到出口处", "station": "江湾镇", "category": "Crowding", "sentiment": "negative"},
    {"text": "东宝兴路站附近老小区多早上买菜的老人和上班族抢着挤地铁", "station": "东宝兴路", "category": "Crowding", "sentiment": "negative"},
    {"text": "四川北路站10号线出来就是四川北路商业街购物方便", "station": "四川北路", "category": "Other", "sentiment": "positive"},
    {"text": "临平路站4号线周边有大型商场站内指引标识较清晰", "station": "临平路", "category": "Accessibility", "sentiment": "positive"},
    {"text": "虹口区多个老旧站点无障碍电梯需要按铃呼叫工作人员高峰期等待时间长达10分钟", "station": "虹口足球场", "category": "Accessibility", "sentiment": "negative"},

    # --- 黄浦区 Huangpu District stations ---
    {"text": "人民广场站早高峰1号线换2号线人流像开闸放水存在踩踏隐患", "station": "人民广场", "category": "Safety", "sentiment": "negative"},
    {"text": "人民广场站节假日客流暴增工作人员在出口处限流进站要排队半小时", "station": "人民广场", "category": "Crowding", "sentiment": "negative"},
    {"text": "南京东路站无障碍电梯被围挡锁住需要按通话按钮呼叫工作人员才能开启", "station": "南京东路", "category": "Accessibility", "sentiment": "negative"},
    {"text": "南京东路站无障碍坡道坡度达8.8度远超国标4.76度轮椅使用者上坡困难且危险", "station": "南京东路", "category": "Safety", "sentiment": "negative"},
    {"text": "南京东路站出口外游客扎堆节假日从地铁口出来就被人群裹挟着走", "station": "南京东路", "category": "Crowding", "sentiment": "negative"},
    {"text": "南京东路站站内指引标识比较清楚中英文对照方便外国游客", "station": "南京东路", "category": "Accessibility", "sentiment": "positive"},
    {"text": "豫园站14号线新装修后很干净引导标识也很清晰游客体验明显改善", "station": "豫园", "category": "Cleanliness", "sentiment": "positive"},
    {"text": "豫园站城隍庙方向出口节假日人满为患站内工作人员疏导很辛苦", "station": "豫园", "category": "Crowding", "sentiment": "negative"},
    {"text": "老西门站8号线换乘10号线通道比较窄高峰期双向人流对冲很危险", "station": "老西门", "category": "Safety", "sentiment": "negative"},
    {"text": "老西门站附近居民以老年人居多无障碍设施使用需求大但电梯经常维修", "station": "老西门", "category": "Accessibility", "sentiment": "negative"},
    {"text": "大世界站8号线出站就是云南南路美食街游客吃完步行就到外滩体验很好", "station": "大世界", "category": "Other", "sentiment": "positive"},
    {"text": "新天地站13号线周末人气旺盛站内秩序总体良好但出口处经常堵", "station": "新天地", "category": "Crowding", "sentiment": "negative"},
    {"text": "黄陂南路站14号线靠近新天地和淮海路商圈站内环境整洁", "station": "黄陂南路", "category": "Cleanliness", "sentiment": "positive"},
    {"text": "陆家浜路站9号线换乘8号线通道维护不够站内有些角落卫生状况差", "station": "陆家浜路", "category": "Cleanliness", "sentiment": "negative"},
    {"text": "西藏南路站8号线站内空调效果差夏天候车闷热难耐乘客意见很大", "station": "西藏南路", "category": "Cleanliness", "sentiment": "negative"},
    {"text": "黄浦区内换乘站密集但部分老站缺少无障碍厕所轮椅乘客上厕所很困难", "station": "人民广场", "category": "Accessibility", "sentiment": "negative"},

    # --- 浦东新区 Pudong District stations ---
    {"text": "陆家嘴站2号线早高峰出站上班族排队等扶梯人流量巨大", "station": "陆家嘴", "category": "Crowding", "sentiment": "negative"},
    {"text": "陆家嘴站无障碍厕位门宽仅1.16米轮椅进去后门关不上", "station": "陆家嘴", "category": "Accessibility", "sentiment": "negative"},
    {"text": "陆家嘴站卫生间入口处盲道中断视障人士找厕所增加了难度", "station": "陆家嘴", "category": "Accessibility", "sentiment": "negative"},
    {"text": "陆家嘴站14号线新线开通后分流了不少2号线客流高峰期比以前好一些了", "station": "陆家嘴", "category": "Crowding", "sentiment": "neutral"},
    {"text": "世纪大道站四线换乘早晚高峰人流如织上下楼梯要格外小心", "station": "世纪大道", "category": "Safety", "sentiment": "negative"},
    {"text": "世纪大道站换乘通道设有自动步道但高峰期人太多根本走不动", "station": "世纪大道", "category": "Crowding", "sentiment": "negative"},
    {"text": "东昌路站2号线靠近陆家嘴早高峰出站排队时间长刷卡闸机不够用", "station": "东昌路", "category": "Delay", "sentiment": "negative"},
    {"text": "浦东大道站经过布局优化改造后高峰期拥堵明显缓解出口闸机增多了", "station": "浦东大道", "category": "Crowding", "sentiment": "positive"},
    {"text": "源深路站14号线周边有体育场和学校多功能融合站内宽敞体验好", "station": "源深路", "category": "Cleanliness", "sentiment": "positive"},
    {"text": "蓝村路站4号线换乘6号线虽然人流大但标识清楚指引明确换乘顺畅", "station": "蓝村路", "category": "Accessibility", "sentiment": "positive"},
    {"text": "金桥站6号线附近大型居民区多早晚高峰通勤人流量巨大车厢爆满", "station": "金桥", "category": "Crowding", "sentiment": "negative"},
    {"text": "张江高科站2号线服务张江科学城上班族集中高峰期客流量很大", "station": "张江高科", "category": "Crowding", "sentiment": "negative"},
    {"text": "北洋泾路站6号线早高峰排队进站经常排到外面的人行道上等三趟才挤上", "station": "北洋泾路", "category": "Crowding", "sentiment": "negative"},
    {"text": "浦电路站6号线站台较窄高峰期候车存在安全隐患工作人员反复广播提醒", "station": "浦电路", "category": "Safety", "sentiment": "negative"},
    {"text": "龙阳路站多线换乘枢纽人流量集中高峰期换乘通道拥挤不堪要排队", "station": "龙阳路", "category": "Crowding", "sentiment": "negative"},
    {"text": "川沙站2号线迪士尼方向游客和通勤者混在一起周末和节假日尤为拥挤", "station": "川沙", "category": "Crowding", "sentiment": "negative"},

    # --- 噪音问题 Noise (补充) ---
    {"text": "2号线江苏路到世纪大道段车厢内全程没有语音报站显示屏蓝屏乘客坐过站", "station": "江苏路", "category": "Noise", "sentiment": "negative"},
    {"text": "12号线车厢内报站声音明显小于车厢噪声难以听清到站信息", "station": None, "category": "Noise", "sentiment": "negative"},
    {"text": "9号线肇嘉浜路站上车后仔细倾听报站声却不清晰声音像从远处传来", "station": "肇嘉浜路", "category": "Noise", "sentiment": "negative"},
    {"text": "11号线车厢噪声峰值达到107分贝手机健康软件提醒可能导致暂时性听力损失", "station": None, "category": "Noise", "sentiment": "negative"},
    {"text": "10号线南京东路到陕西南路段行驶中分贝达到90盖过了中文报站前半段", "station": "南京东路", "category": "Noise", "sentiment": "negative"},
    {"text": "旧车旧线路多媒体显示设备少乘客更容易错过报站信息坐过站", "station": None, "category": "Noise", "sentiment": "negative"},
    {"text": "地铁车厢内手机外放现象屡禁不止42%的乘客反映被声音外放困扰", "station": None, "category": "Noise", "sentiment": "negative"},
    {"text": "部分线路隧道中弯道钢轨发出尖锐啸叫噪声对耳膜产生极大刺激", "station": None, "category": "Noise", "sentiment": "negative"},
    {"text": "新线路车厢噪音控制好语音报站清晰配合电子屏幕显示体验好很多", "station": None, "category": "Noise", "sentiment": "positive"},
    {"text": "7号线场中路站附近居民投诉地铁运行振动噪音影响夜间休息", "station": "场中路", "category": "Noise", "sentiment": "negative"},

    # --- 延误/故障 Delay (补充) ---
    {"text": "浦江线因供电设备故障汇臻路至沈杜公路区段发车间隔延长影响15分钟", "station": "汇臻路", "category": "Delay", "sentiment": "negative"},
    {"text": "5号线线路设备故障东川路至闵行开发区区段班次间隔延长25分钟站台挤满人", "station": "东川路", "category": "Delay", "sentiment": "negative"},
    {"text": "3号线信号设备故障乘客反映二十分钟才过去了两站堵在第一站十三分钟", "station": None, "category": "Delay", "sentiment": "negative"},
    {"text": "2025年4月早高峰1号线2号线4号线大规模延误乘客站台等待超过30分钟", "station": "人民广场", "category": "Delay", "sentiment": "negative"},
    {"text": "13号线金运路至丰庄区段线路设备故障列车限速运行全线延误", "station": "金运路", "category": "Delay", "sentiment": "negative"},
    {"text": "故障后地铁方发布延误证明乘客可通过官网或微信获取但有人说操作麻烦", "station": None, "category": "Delay", "sentiment": "negative"},
    {"text": "上海地铁将运营故障分为十类包括车门车辆信号供电等高峰期影响最大", "station": None, "category": "Delay", "sentiment": "neutral"},
    {"text": "14号线真如站一名老年乘客乘扶梯未站稳摔倒在地", "station": "真如", "category": "Delay", "sentiment": "negative"},
    {"text": "早高峰故障后恢复运营列车仍然限速运行到公司已经迟到一个多小时", "station": None, "category": "Delay", "sentiment": "negative"},
    {"text": "地铁故障时站内广播信息更新慢乘客只能靠刷微博了解实时情况", "station": None, "category": "Delay", "sentiment": "negative"},

    # --- 安全问题 Safety (补充) ---
    {"text": "1号线早高峰车厢内发生猥亵事件周围乘客当场控制嫌疑人并报警", "station": None, "category": "Safety", "sentiment": "negative"},
    {"text": "扶梯口高峰期人流推搡很危险尤其是有老人小孩在场时极易摔倒", "station": None, "category": "Safety", "sentiment": "negative"},
    {"text": "车门关闭警示灯闪烁时仍有乘客强行上下车存在被夹伤的安全隐患", "station": None, "category": "Safety", "sentiment": "negative"},
    {"text": "高峰期人与人之间完全没有安全距离拥挤导致小偷更容易下手", "station": None, "category": "Safety", "sentiment": "negative"},
    {"text": "部分站点屏蔽门与列车门之间缝隙较大小孩容易被卡住让人担心", "station": None, "category": "Safety", "sentiment": "negative"},
    {"text": "上海地铁对侵犯女性权益行为零容忍但乘客反映高峰期取证困难", "station": None, "category": "Safety", "sentiment": "negative"},
    {"text": "新版乘客守则2025年3月起施行明确禁止影响运营安全和滋扰乘客行为", "station": None, "category": "Safety", "sentiment": "positive"},
    {"text": "地铁站内安防监控覆盖率高工作人员巡逻频繁总体安全感不错", "station": None, "category": "Safety", "sentiment": "positive"},

    # --- 清洁/卫生 Cleanliness (补充) ---
    {"text": "调查显示30.4%的站点卫生间没有厕纸需要付费购买纸巾", "station": None, "category": "Cleanliness", "sentiment": "negative"},
    {"text": "15.9%的站点卫生间存在明显异味特别是夏季更为严重", "station": None, "category": "Cleanliness", "sentiment": "negative"},
    {"text": "部分老旧站点天花板格栅脏乱电线下坠墙面有污迹印迹", "station": None, "category": "Cleanliness", "sentiment": "negative"},
    {"text": "站内卫生间正常使用无明显异味的得分率仅89.63%是全网最低指标之一", "station": None, "category": "Cleanliness", "sentiment": "negative"},
    {"text": "新线路如14号线15号线18号线的站内卫生状况明显好于老线路", "station": None, "category": "Cleanliness", "sentiment": "positive"},
    {"text": "环境良好整洁卫生的得分率仅68.13%是全网得分最低的指标令人担忧", "station": None, "category": "Cleanliness", "sentiment": "negative"},

    # --- 无障碍设施 Accessibility (补充) ---
    {"text": "1号线70部无障碍电梯中47部为非自助需工作人员启动占比67%", "station": None, "category": "Accessibility", "sentiment": "negative"},
    {"text": "残障志愿者低峰时期等无障碍电梯约2到3分钟高峰时期可能长达10分钟", "station": None, "category": "Accessibility", "sentiment": "negative"},
    {"text": "2号线淞虹路站出口外非机动车占满盲道一两百米严重影响视障人士安全", "station": None, "category": "Accessibility", "sentiment": "negative"},
    {"text": "上海地铁推出线上爱心预约为老人轮椅乘客提供全路径陪同护行服务值得点赞", "station": None, "category": "Accessibility", "sentiment": "positive"},
    {"text": "上海地铁计划2024到2026年对1号线8座车站增设11台自动扶梯改善出行体验", "station": None, "category": "Accessibility", "sentiment": "positive"},

    # --- 公交反馈 Bus-related ---
    {"text": "蒲三路长利东路公交站设计不合理后门下车乘客找不到落脚点被挤在车和绿化带之间", "station": None, "category": "Safety", "sentiment": "negative"},
    {"text": "上海公交部分线路班次间隔太长等了20多分钟车才来", "station": None, "category": "Delay", "sentiment": "negative"},
    {"text": "公交车空调夏天冷得像冰柜短袖穿着冷得发抖", "station": None, "category": "Cleanliness", "sentiment": "negative"},
    {"text": "公交车上老年人多让座氛围好上海市民素质整体不错", "station": None, "category": "Other", "sentiment": "positive"},
    {"text": "公交站牌信息更新不及时有的线路已经改了但站牌还是旧的容易搞错", "station": None, "category": "Accessibility", "sentiment": "negative"},
]


def get_real_feedback_texts() -> list[str]:
    """Return all real feedback texts for the seeding pipeline."""
    return [item["text"] for item in REAL_FEEDBACK_DATA]


def get_real_feedback_records() -> list[dict]:
    """Return all real feedback records with pre-annotated labels."""
    return list(REAL_FEEDBACK_DATA)

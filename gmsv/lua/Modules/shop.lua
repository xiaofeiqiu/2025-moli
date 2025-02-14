local Shop = ModuleBase:createModule('shop')

function Shop:onLoad()
  self:logInfo('load')
  local shopConfig = { sellTypes = 'all' };
  self:NPC_createShop('¿óÊ¯··Âô', 104863, { map = 1000, mapType = 0, x = 235, y = 86, direction = 4 }, shopConfig, {
    9600, 9601, 9602, 9603, 9604, 9605, 9606, 9607, 9608, 9609,
    9610, 9625, 9630, 9708, 9639, 9641, 9637, 9630, 18509
  });
  self:NPC_createShop('¿óÌõ··Âô', 104863, { map = 1000, mapType = 0, x = 237, y = 86, direction = 4 }, shopConfig, {
    9611, 9612, 9613, 9614, 9615, 9616, 9617, 9618, 9619, 9620,
    9621, 9700, 9638, 9640, 9642,
  });
  self:NPC_createShop('Ä¾²Ä··Âô', 104863, { map = 1000, mapType = 0, x = 233, y = 86, direction = 4 }, shopConfig, {
    10000, 10001, 10002, 10100, 10003, 10004, 10005, 10006, 10007, 10008,
    10009, 10010, 10011,
  });
  self:NPC_createShop('Æ¤²¼··Âô', 104863, { map = 1000, mapType = 0, x = 231, y = 86, direction = 4 }, shopConfig, {
    18211, 12415, 18634, 10400, 10401, 10402, 10403, 10404, 10405, 10406,
    10407, 10408, 10409, 10410, 10411, 40738, 40739, 40740, 40741, 40742,
  });
  self:NPC_createShop('Æ¤²¼··Âô', 104863, { map = 1000, mapType = 0, x = 229, y = 86, direction = 4 }, shopConfig, {
    40743, 40744, 40745, 40746, 40747, 40748,
  });
  self:NPC_createShop('»¨²Ý··Âô', 104863, { map = 1000, mapType = 0, x = 227, y = 86, direction = 4 }, shopConfig, {
    12800, 12801, 12802, 12803, 12804, 12805, 12806, 12807, 12808, 12809,
    12810, 12811, 12822
  });
  self:NPC_createShop('Ë®Áú··Âô', 104863, { map = 1000, mapType = 0, x = 225, y = 86, direction = 4 }, shopConfig, {
    18851, 18852, 18853, 18854, 18855, 18856, 18857, 18858, 18859, 18860,
    18861, 18862, 18863, 18864, 18865, 18866, 18867, 18843
  });
  self:NPC_createShop('ÆäËû··Âô', 104863, { map = 1000, mapType = 0, x = 223, y = 86, direction = 4 }, shopConfig, {
    --18442,
    18449, 18450, 18451, 18452, 18453, 18454, 18455, 18456, 40042, 16378,
    16379, 18310, 18311, 18312, 18313, 18443, 18195, 18795
    --18457, 18458, 18459
  });
  self:NPC_createShop('Ò©Æ···Âô', 104863, { map = 1000, mapType = 0, x = 237, y = 91, direction = 0 }, shopConfig, {
    15605, 15606, 15607, 15608, 15609, 15610, 15611, 15612, 15613, 15614,
    15615, 18567
  });
  self:NPC_createShop('ÁÏÀí··Âô', 104863, { map = 1000, mapType = 0, x = 235, y = 91, direction = 0 }, shopConfig, {
    15201, 15202, 15203, 15204, 15205, 15206, 15207, 15208, 15209, 15210,
    15211, 15212, 15213, 15214, 15215, 15216, 15217, 15218, 15219,
  });
  self:NPC_createShop('±¦Ê¯··Âô', 104863, { map = 1000, mapType = 0, x = 233, y = 91, direction = 0 }, shopConfig, {
    13609, 13619, 13629, 13639, 13649, 13659, 13669, 13679, 18375, 18658,
    18699, 40949, 40962, 40963, 46074, 606209, 606219, 606229, 606239, 606249,
  });
  self:NPC_createShop('±¦Ê¯··Âô', 104863, { map = 1000, mapType = 0, x = 231, y = 91, direction = 0 }, shopConfig, {
    606259, 606269, 606279, 606289, 606299, 606309, 606319, 606328,
  });
  self:NPC_createShop('Ë®¾§··Âô', 104863, { map = 1000, mapType = 0, x = 229, y = 91, direction = 0 }, shopConfig, {
    9201, 9202, 9203, 9204, 9209, 9218, 9227, 9236, 46630, 46631,
    46632, 46633, 46634, 46635, 46636, 46637, 9315
  });
  self:NPC_createShop('·âÓ¡··Âô', 104863, { map = 1000, mapType = 0, x = 227, y = 91, direction = 0 }, shopConfig, {
    14409, 14419, 14429, 14439, 14449, 14459, 14469, 14479, 14489,
    14499,
  });
  self:NPC_createShop('²ÊÆ±··Âô', 104863, { map = 1000, mapType = 0, x = 225, y = 91, direction = 0 }, shopConfig, {
    47763, 16000, 16001, 16002, 45950, 45981, 45969
  });
  self:NPC_createShop('±äÉí··Âô', 104863, { map = 1000, mapType = 0, x = 223, y = 91, direction = 0 }, shopConfig, {
    46329, 70001,
  });

  self:NPC_createShop('¹­¼ýµê', 104863, { map = 1000, mapType = 0, x = 221, y = 91, direction = 4 }, shopConfig, {
    2000,2002,2010,2017,2022,2023,2035,2038,2049,2042,
    2055,2052,2063,2062,2071,2078,2082,2083,2095,2098
  });

  self:NPC_createShop('¹­¼ýµê2', 104863, { map = 1000, mapType = 0, x = 219, y = 91, direction = 4 }, shopConfig, {
    2070,215,217,600602,600615,600616
  });

  self:NPC_createShop('·¨ÕÈµê', 104863, { map = 1000, mapType = 0, x = 217, y = 91, direction = 4 }, shopConfig, {
    2404,2402,2413,2418,2435,2434,2447,2446,2449,2450,
    2461,2462,2473,2478,2488,2486,2492,2495,2493,2497
  });

  self:NPC_createShop('·¨ÕÈµê2', 104863, { map = 1000, mapType = 0, x = 215, y = 91, direction = 4 }, shopConfig, {
    2484,220,263,600802,600815,600816
  });

  self:NPC_createShop('Ã±×Óµê', 104863, { map = 1000, mapType = 0, x = 213, y = 91, direction = 4 }, shopConfig, {
    4004,4001,4011,4013,4022,4020,4032,4031,4040,4042,
    4054,4051,4064,4062,4070,4074,4082,4084,4091,4092
  });

  self:NPC_createShop('Ñ¥×Ó', 104863, { map = 1000, mapType = 0, x = 210, y = 91, direction = 4 }, shopConfig, {
    5600,5601,5614,5612,5620,5621,5630,5631,5640,5641,
    5653,5654,5664,5660,5671,5673,5680,5681,5690,5691,
  });

  self:NPC_createShop('Ñ¥×Ó2', 104863, { map = 1000, mapType = 0, x = 208, y = 91, direction = 4 }, shopConfig, {
    5675,260,262,602400,602415,602416
  });

  self:NPC_createShop('¶Ü', 104863, { map = 1000, mapType = 0, x = 206, y = 91, direction = 4 }, shopConfig, {
    6401,6402,6410,6412,6427,6425,6437,6434,6447,6449,
    6458,6457,6461,6463,6470,6477,6480,6481,6490,6491,
  });

  self:NPC_createShop('¶Ü2', 104863, { map = 1000, mapType = 0, x = 204, y = 91, direction = 4 }, shopConfig, {
    6473,270,272,602800,602815,602816
  });

  self:NPC_createShop('Ã±×Óµê2', 104863, { map = 1000, mapType = 0, x = 221, y = 86, direction = 4 }, shopConfig, {
    4075,240,241,242,601600,601615,601616
  });

  self:NPC_createShop('ÒÂ·þµê', 104863, { map = 1000, mapType = 0, x = 219, y = 86, direction = 4 }, shopConfig, {
    4803,4806,4812,4813,4823,4821,4834,4833,4845,4844,
    4855,4853,4860,4867,4871,4873,4882,4883,4892,4893
  });

  self:NPC_createShop('ÒÂ·þµê2', 104863, { map = 1000, mapType = 0, x = 217, y = 86, direction = 4 }, shopConfig, {
    4877,250,252,602001,602015,602016
  });

  self:NPC_createShop('·¨ÅÛµê', 104863, { map = 1000, mapType = 0, x = 215, y = 86, direction = 4 }, shopConfig, {
    5206,5205,5212,5211,5224,5223,5233,5231,5242,5244,
    5250,5253,5261,5262,5272,5274,5281,5282,5290,5291
  });

  self:NPC_createShop('·¨ÅÛµê2', 104863, { map = 1000, mapType = 0, x = 213, y = 86, direction = 4 }, shopConfig, {
    5275,255,257,602200,602215,602216
  });

  self:NPC_createShop('Ð¬×Óµê', 104863, { map = 1000, mapType = 0, x = 211, y = 86, direction = 4 }, shopConfig, {
    6001,6002,6010,6011,6022,6025,6033,6031,6042,6040,
    6054,6052,6064,6063,6072,6074,6080,6081,6090,6091
  });

  self:NPC_createShop('Ð¬×Óµê2', 104863, { map = 1000, mapType = 0, x = 209, y = 86, direction = 4 }, shopConfig, {
    6075,265,803,602601,602615
  });

  self:NPC_createShop('½£', 104863, { map = 1000, mapType = 0, x = 207, y = 86, direction = 4 }, shopConfig, {
    8, 3, 16, 18, 22, 28, 37, 39, 42, 48,
     56, 57, 67, 63, 70, 77, 88, 87, 94, 97,
     73, 200, 202, 600002, 600015, 600016
  });

  self:NPC_createShop('½£2', 104863, { map = 1000, mapType = 0, x = 205, y = 86, direction = 4 }, shopConfig, {
     73, 200, 202, 600002, 600015, 600016
  });

  self:NPC_createShop('Í·¿ø', 104863, { map = 1000, mapType = 0, x = 203, y = 86, direction = 4 }, shopConfig, {
    3601,3602,3611,3612,3622,3620,3632,3635,3642,3640,
    3654,3651,3662,3664,3670,3671,3683,3682,3693,3692,
 });

 self:NPC_createShop('Í·¿ø2', 104863, { map = 1000, mapType = 0, x = 201, y = 86, direction = 4 }, shopConfig, {
  3675,235,237,601400,601415,601416
});

self:NPC_createShop('îø¼×', 104863, { map = 1000, mapType = 0, x = 199, y = 86, direction = 4 }, shopConfig, {
  4400,4405,4410,4411,4420,4421,4430,4434,4442,4444,
  4459,4458,4464,4461,4470,4471,4484,4481,4490,4491,
});

self:NPC_createShop('îø¼×2', 104863, { map = 1000, mapType = 0, x = 197, y = 86, direction = 4 }, shopConfig, {
  4475,245,247,601800,601815,601816
});

self:NPC_createShop('Ç¹', 104863, { map = 1000, mapType = 0, x = 202, y = 91, direction = 4 }, shopConfig, {
  1608,1606,1619,1613,1629,1625,1635,1634,1643,1649,
  1657,1658,1663,1669,1678,1673,1684,1686,1698,1695,
});

self:NPC_createShop('Ç¹2', 104863, { map = 1000, mapType = 0, x = 200, y = 91, direction = 4 }, shopConfig, {
1672,210,212,600402,600415,600416,
});

self:NPC_createShop('¸«1', 104863, { map = 1000, mapType = 0, x = 212, y = 83, direction = 4 }, shopConfig, {
  805, 809, 812, 811, 820, 826, 830, 838, 841, 842,
  854, 852, 863, 867, 878, 872, 883, 885, 890, 895,
});

self:NPC_createShop('¸«2', 104863, { map = 1000, mapType = 0, x = 210, y = 83, direction = 4 }, shopConfig, {
875, 205, 207, 600202, 600215, 600216
});

end

function Shop:onUnload()
  self:logInfo('unload')
end

return Shop;

#pragma once
namespace LightGBM { 
		class CovTypeClassifier {
		public:
			float predict(const float values[25]) {
				float result = 0;
				float thresholds[459];
				thresholds[0] =3086.5;
				thresholds[1] =2497.5;
				thresholds[2] =3196.5;
				thresholds[3] =3021.5;
				thresholds[4] =1e-35;
				thresholds[5] =5372.5;
				thresholds[6] =166;
				thresholds[7] =4574.5;
				thresholds[8] =1192.5;
				thresholds[9] =3296.5;
				thresholds[10] =2429.5;
				thresholds[11] =690.5;
				thresholds[12] =-0.161272;
				thresholds[13] =-0.0710885;
				thresholds[14] =0.120769;
				thresholds[15] =-0.118646;
				thresholds[16] =-0.0181189;
				thresholds[17] =-0.157159;
				thresholds[18] =-0.0920923;
				thresholds[19] =0.0606127;
				thresholds[20] =-0.0921708;
				thresholds[21] =0.0645619;
				thresholds[22] =0.0723188;
				thresholds[23] =0.146951;
				thresholds[24] =-0.168243;
				thresholds[25] =-0.0692163;
				thresholds[26] =-0.167249;
				thresholds[27] =-0.177664;
				thresholds[28] =3089.5;
				thresholds[29] =3011.5;
				thresholds[30] =3211.5;
				thresholds[31] =5544.5;
				thresholds[32] =419;
				thresholds[33] =1370.5;
				thresholds[34] =1235.5;
				thresholds[35] =3308.5;
				thresholds[36] =2451.5;
				thresholds[37] =-0.172823;
				thresholds[38] =-0.0894471;
				thresholds[39] =0.0897644;
				thresholds[40] =-0.00920045;
				thresholds[41] =-0.135771;
				thresholds[42] =-0.163255;
				thresholds[43] =-0.131917;
				thresholds[44] =0.0280595;
				thresholds[45] =0.0922438;
				thresholds[46] =0.0788135;
				thresholds[47] =-0.0904719;
				thresholds[48] =0.121982;
				thresholds[49] =-0.176165;
				thresholds[50] =-0.0644099;
				thresholds[51] =-0.16707;
				thresholds[52] =0.208725;
				thresholds[53] =3098.5;
				thresholds[54] =3034.5;
				thresholds[55] =3194.5;
				thresholds[56] =3218.5;
				thresholds[57] =217;
				thresholds[58] =211;
				thresholds[59] =3292.5;
				thresholds[60] =181;
				thresholds[61] =704.5;
				thresholds[62] =-0.153315;
				thresholds[63] =-0.0790494;
				thresholds[64] =0.0669627;
				thresholds[65] =-0.0433815;
				thresholds[66] =-0.115855;
				thresholds[67] =0.14616;
				thresholds[68] =-0.158131;
				thresholds[69] =-0.0026153;
				thresholds[70] =-0.0978803;
				thresholds[71] =0.0285322;
				thresholds[72] =0.0433494;
				thresholds[73] =-0.159151;
				thresholds[74] =-0.0562179;
				thresholds[75] =-0.141206;
				thresholds[76] =-0.0828172;
				thresholds[77] =-0.169011;
				thresholds[78] =3073.5;
				thresholds[79] =241.5;
				thresholds[80] =2942.5;
				thresholds[81] =3151.5;
				thresholds[82] =4610.5;
				thresholds[83] =5416.5;
				thresholds[84] =3263.5;
				thresholds[85] =151.5;
				thresholds[86] =-0.142564;
				thresholds[87] =-0.04669;
				thresholds[88] =0.0746022;
				thresholds[89] =-0.100261;
				thresholds[90] =0.0383207;
				thresholds[91] =-0.0852242;
				thresholds[92] =0.0090567;
				thresholds[93] =-0.0788433;
				thresholds[94] =-0.088403;
				thresholds[95] =-0.138335;
				thresholds[96] =0.0404023;
				thresholds[97] =0.141017;
				thresholds[98] =-0.142622;
				thresholds[99] =-0.0456733;
				thresholds[100] =-0.125143;
				thresholds[101] =-0.158006;
				thresholds[102] =3101.5;
				thresholds[103] =237.5;
				thresholds[104] =2948.5;
				thresholds[105] =3323.5;
				thresholds[106] =2627.5;
				thresholds[107] =-0.140731;
				thresholds[108] =-0.109873;
				thresholds[109] =0.0642665;
				thresholds[110] =0.0328174;
				thresholds[111] =-0.0802869;
				thresholds[112] =-0.119579;
				thresholds[113] =-0.0643964;
				thresholds[114] =0.0175071;
				thresholds[115] =-0.0720897;
				thresholds[116] =0.00329201;
				thresholds[117] =-0.0786746;
				thresholds[118] =0.235517;
				thresholds[119] =0.120848;
				thresholds[120] =-0.0391369;
				thresholds[121] =-0.147391;
				thresholds[122] =-0.120745;
				thresholds[123] =3070.5;
				thresholds[124] =2515.5;
				thresholds[125] =3204.5;
				thresholds[126] =63.5;
				thresholds[127] =5328.5;
				thresholds[128] =1589.5;
				thresholds[129] =1611.5;
				thresholds[130] =721.5;
				thresholds[131] =6302.5;
				thresholds[132] =5154.5;
				thresholds[133] =-0.134001;
				thresholds[134] =-0.0628386;
				thresholds[135] =-0.00151958;
				thresholds[136] =-0.0111626;
				thresholds[137] =0.128753;
				thresholds[138] =0.0559877;
				thresholds[139] =-0.0282595;
				thresholds[140] =0.0412446;
				thresholds[141] =0.0624162;
				thresholds[142] =0.127353;
				thresholds[143] =-0.0735051;
				thresholds[144] =0.165617;
				thresholds[145] =-0.116541;
				thresholds[146] =0.0313901;
				thresholds[147] =-0.0834835;
				thresholds[148] =-0.160889;
				thresholds[149] =3135.5;
				thresholds[150] =2473.5;
				thresholds[151] =3004.5;
				thresholds[152] =191;
				thresholds[153] =3300.5;
				thresholds[154] =241;
				thresholds[155] =236.5;
				thresholds[156] =5161.5;
				thresholds[157] =-0.135784;
				thresholds[158] =-0.101575;
				thresholds[159] =0.0607969;
				thresholds[160] =-0.0426151;
				thresholds[161] =-0.100572;
				thresholds[162] =0.0240416;
				thresholds[163] =-0.108276;
				thresholds[164] =-0.0620962;
				thresholds[165] =0.0196486;
				thresholds[166] =-0.0344155;
				thresholds[167] =0.217795;
				thresholds[168] =0.223161;
				thresholds[169] =-0.110718;
				thresholds[170] =-0.134757;
				thresholds[171] =-0.106816;
				thresholds[172] =0.267842;
				thresholds[173] =3150.5;
				thresholds[174] =3042.5;
				thresholds[175] =243.5;
				thresholds[176] =1807.5;
				thresholds[177] =992.5;
				thresholds[178] =231;
				thresholds[179] =1051;
				thresholds[180] =-0.118169;
				thresholds[181] =-0.0750288;
				thresholds[182] =0.0502495;
				thresholds[183] =-0.0296684;
				thresholds[184] =-0.177019;
				thresholds[185] =0.0585714;
				thresholds[186] =-0.100987;
				thresholds[187] =-0.135174;
				thresholds[188] =-0.100971;
				thresholds[189] =-0.0397974;
				thresholds[190] =0.111687;
				thresholds[191] =0.0168262;
				thresholds[192] =-0.0148497;
				thresholds[193] =0.19868;
				thresholds[194] =0.223398;
				thresholds[195] =0.228481;
				thresholds[196] =3158.5;
				thresholds[197] =2991.5;
				thresholds[198] =233.5;
				thresholds[199] =316;
				thresholds[200] =1035;
				thresholds[201] =3353.5;
				thresholds[202] =3419.5;
				thresholds[203] =-0.117764;
				thresholds[204] =0.00876327;
				thresholds[205] =0.0213545;
				thresholds[206] =-0.0398739;
				thresholds[207] =0.0728375;
				thresholds[208] =0.0244577;
				thresholds[209] =-0.11197;
				thresholds[210] =-0.0605069;
				thresholds[211] =0.0198072;
				thresholds[212] =-0.0898434;
				thresholds[213] =0.146522;
				thresholds[214] =0.210352;
				thresholds[215] =-0.07156;
				thresholds[216] =-0.15524;
				thresholds[217] =-0.129475;
				thresholds[218] =-0.0738873;
				thresholds[219] =3053.5;
				thresholds[220] =101.5;
				thresholds[221] =3217.5;
				thresholds[222] =4125;
				thresholds[223] =1649;
				thresholds[224] =5202.5;
				thresholds[225] =-0.113423;
				thresholds[226] =-0.0545045;
				thresholds[227] =-0.00950936;
				thresholds[228] =0.0567;
				thresholds[229] =-0.097426;
				thresholds[230] =-0.163488;
				thresholds[231] =-0.120059;
				thresholds[232] =0.00636047;
				thresholds[233] =0.0886941;
				thresholds[234] =0.0894305;
				thresholds[235] =-0.0563717;
				thresholds[236] =0.0430448;
				thresholds[237] =0.13796;
				thresholds[238] =0.179968;
				thresholds[239] =-0.0655383;
				thresholds[240] =-0.138881;
				thresholds[241] =3161.5;
				thresholds[242] =2922.5;
				thresholds[243] =234.5;
				thresholds[244] =337;
				thresholds[245] =288.5;
				thresholds[246] =3341.5;
				thresholds[247] =-0.120042;
				thresholds[248] =0.0114119;
				thresholds[249] =0.0255027;
				thresholds[250] =0.0192066;
				thresholds[251] =0.100312;
				thresholds[252] =-0.10062;
				thresholds[253] =-0.0677484;
				thresholds[254] =-0.0487181;
				thresholds[255] =0.027862;
				thresholds[256] =-0.0798085;
				thresholds[257] =0.159407;
				thresholds[258] =-0.0956635;
				thresholds[259] =0.144706;
				thresholds[260] =-0.0917853;
				thresholds[261] =-0.121293;
				thresholds[262] =-0.112036;
				thresholds[263] =3050.5;
				thresholds[264] =5285.5;
				thresholds[265] =2679.5;
				thresholds[266] =2083.5;
				thresholds[267] =2407.5;
				thresholds[268] =-0.107859;
				thresholds[269] =-0.0502616;
				thresholds[270] =-0.00784781;
				thresholds[271] =-0.20465;
				thresholds[272] =0.0478684;
				thresholds[273] =-0.0819773;
				thresholds[274] =0.0557546;
				thresholds[275] =0.0341447;
				thresholds[276] =-0.0190071;
				thresholds[277] =-0.0268161;
				thresholds[278] =0.129412;
				thresholds[279] =-0.0620734;
				thresholds[280] =0.147899;
				thresholds[281] =-0.127957;
				thresholds[282] =-0.115376;
				thresholds[283] =-0.0912835;
				thresholds[284] =2815.5;
				thresholds[285] =235.5;
				thresholds[286] =658.5;
				thresholds[287] =4106.5;
				thresholds[288] =-0.0900703;
				thresholds[289] =-0.0874105;
				thresholds[290] =0.0214114;
				thresholds[291] =0.0598594;
				thresholds[292] =0.0918207;
				thresholds[293] =-0.0948335;
				thresholds[294] =-0.0519152;
				thresholds[295] =-0.0471484;
				thresholds[296] =0.0134865;
				thresholds[297] =-0.0350919;
				thresholds[298] =-0.00946676;
				thresholds[299] =-0.105252;
				thresholds[300] =0.135995;
				thresholds[301] =-0.118396;
				thresholds[302] =-0.116667;
				thresholds[303] =-0.114183;
				thresholds[304] =3047.5;
				thresholds[305] =239.5;
				thresholds[306] =3290.5;
				thresholds[307] =2672.5;
				thresholds[308] =1156.5;
				thresholds[309] =403;
				thresholds[310] =0.0351989;
				thresholds[311] =-0.030409;
				thresholds[312] =-0.0737355;
				thresholds[313] =-0.185474;
				thresholds[314] =-0.157702;
				thresholds[315] =-0.071792;
				thresholds[316] =0.0015295;
				thresholds[317] =-0.105112;
				thresholds[318] =0.0899975;
				thresholds[319] =-0.0224169;
				thresholds[320] =0.0129809;
				thresholds[321] =-0.135106;
				thresholds[322] =0.126267;
				thresholds[323] =-0.109408;
				thresholds[324] =-0.106624;
				thresholds[325] =-0.118693;
				thresholds[326] =3181.5;
				thresholds[327] =2973.5;
				thresholds[328] =346;
				thresholds[329] =2839.5;
				thresholds[330] =1402;
				thresholds[331] =3230.5;
				thresholds[332] =361.5;
				thresholds[333] =0.00527479;
				thresholds[334] =-0.0791794;
				thresholds[335] =-0.0673569;
				thresholds[336] =-0.0244508;
				thresholds[337] =0.0581627;
				thresholds[338] =0.0343843;
				thresholds[339] =-0.0218017;
				thresholds[340] =-0.062283;
				thresholds[341] =0.0703116;
				thresholds[342] =-0.0586902;
				thresholds[343] =0.0931107;
				thresholds[344] =0.13894;
				thresholds[345] =0.153376;
				thresholds[346] =0.011683;
				thresholds[347] =-0.124584;
				thresholds[348] =-0.102992;
				thresholds[349] =3172.5;
				thresholds[350] =2727.5;
				thresholds[351] =232.5;
				thresholds[352] =120.5;
				thresholds[353] =-0.10772;
				thresholds[354] =-0.0720652;
				thresholds[355] =0.0250096;
				thresholds[356] =0.100639;
				thresholds[357] =-0.0645546;
				thresholds[358] =-0.108935;
				thresholds[359] =-0.0435837;
				thresholds[360] =-0.0452248;
				thresholds[361] =0.0102621;
				thresholds[362] =0.0746455;
				thresholds[363] =-0.0828075;
				thresholds[364] =0.189612;
				thresholds[365] =0.106418;
				thresholds[366] =-0.0766807;
				thresholds[367] =-0.080435;
				thresholds[368] =-0.131995;
				thresholds[369] =3122.5;
				thresholds[370] =125.5;
				thresholds[371] =2939.5;
				thresholds[372] =3368.5;
				thresholds[373] =271;
				thresholds[374] =122;
				thresholds[375] =152.5;
				thresholds[376] =0.0119766;
				thresholds[377] =-0.0438321;
				thresholds[378] =-0.0744184;
				thresholds[379] =0.0337251;
				thresholds[380] =-0.14662;
				thresholds[381] =-0.0437443;
				thresholds[382] =-0.0807322;
				thresholds[383] =-0.11306;
				thresholds[384] =0.00113797;
				thresholds[385] =0.0582423;
				thresholds[386] =-0.0668001;
				thresholds[387] =-0.109373;
				thresholds[388] =0.0999667;
				thresholds[389] =0.0362569;
				thresholds[390] =-0.108871;
				thresholds[391] =-0.127632;
				thresholds[392] =2530.5;
				thresholds[393] =51;
				thresholds[394] =87.5;
				thresholds[395] =3407.5;
				thresholds[396] =240.5;
				thresholds[397] =5899.5;
				thresholds[398] =4477.5;
				thresholds[399] =3702.5;
				thresholds[400] =-0.0990378;
				thresholds[401] =-0.0234414;
				thresholds[402] =-0.219303;
				thresholds[403] =-0.0216317;
				thresholds[404] =0.035402;
				thresholds[405] =-0.0131391;
				thresholds[406] =-0.120996;
				thresholds[407] =-0.0564786;
				thresholds[408] =0.0279316;
				thresholds[409] =0.118105;
				thresholds[410] =0.00296039;
				thresholds[411] =-0.0502752;
				thresholds[412] =-0.129784;
				thresholds[413] =-0.0695183;
				thresholds[414] =-0.0982619;
				thresholds[415] =0.138513;
				thresholds[416] =5760.5;
				thresholds[417] =72.5;
				thresholds[418] =4861.5;
				thresholds[419] =-0.0670413;
				thresholds[420] =-0.0743688;
				thresholds[421] =0.0916515;
				thresholds[422] =-0.0149986;
				thresholds[423] =0.0163606;
				thresholds[424] =0.100205;
				thresholds[425] =-0.0681571;
				thresholds[426] =0.123151;
				thresholds[427] =-0.0568073;
				thresholds[428] =0.0698541;
				thresholds[429] =0.052236;
				thresholds[430] =-0.0012757;
				thresholds[431] =-0.128739;
				thresholds[432] =-0.316122;
				thresholds[433] =0.00163008;
				thresholds[434] =-0.106926;
				thresholds[435] =3214.5;
				thresholds[436] =5805.5;
				thresholds[437] =6541.5;
				thresholds[438] =4906.5;
				thresholds[439] =1950.5;
				thresholds[440] =2788.5;
				thresholds[441] =226.5;
				thresholds[442] =455.5;
				thresholds[443] =-0.063778;
				thresholds[444] =0.0650104;
				thresholds[445] =0.0321191;
				thresholds[446] =0.00169797;
				thresholds[447] =0.0836978;
				thresholds[448] =0.0862171;
				thresholds[449] =-0.0271812;
				thresholds[450] =-0.0681434;
				thresholds[451] =-0.191119;
				thresholds[452] =-0.140001;
				thresholds[453] =-0.10547;
				thresholds[454] =0.0973202;
				thresholds[455] =0.130308;
				thresholds[456] =-0.035864;
				thresholds[457] =0.00184129;
				thresholds[458] =0.0842113;
				int features[25];
				features[0] =1;
				features[1] =16;
				features[2] =6;
				features[3] =46;
				features[4] =43;
				features[5] =4;
				features[6] =10;
				features[7] =20;
				features[8] =45;
				features[9] =26;
				features[10] =47;
				features[11] =37;
				features[12] =36;
				features[13] =8;
				features[14] =41;
				features[15] =11;
				features[16] =13;
				features[17] =18;
				features[18] =24;
				features[19] =2;
				features[20] =14;
				features[21] =38;
				features[22] =5;
				features[23] =9;
				features[24] =7;
				// tree 0 ...
				if (values[1] <= thresholds[0]) {
					if (values[1] <= thresholds[1]) {
						if (values[1] <= thresholds[10]) {
							if (values[6] <= thresholds[11]) {
								result += thresholds[12];
							} else {
								result += thresholds[27];
							}
						} else {
							if (values[20] <= thresholds[4]) {
								result += thresholds[25];
							} else {
								result += thresholds[26];
							}
						}
					} else {
						if (values[1] <= thresholds[3]) {
							if (values[16] <= thresholds[4]) {
								result += thresholds[14];
							} else {
								result += thresholds[17];
							}
						} else {
							if (values[4] <= thresholds[6]) {
								result += thresholds[16];
							} else {
								result += thresholds[21];
							}
						}
					}
				} else {
					if (values[1] <= thresholds[2]) {
						if (values[6] <= thresholds[5]) {
							if (values[46] <= thresholds[4]) {
								result += thresholds[13];
							} else {
								result += thresholds[19];
							}
						} else {
							if (values[10] <= thresholds[8]) {
								result += thresholds[18];
							} else {
								result += thresholds[23];
							}
						}
					} else {
						if (values[43] <= thresholds[4]) {
							if (values[1] <= thresholds[9]) {
								result += thresholds[15];
							} else {
								result += thresholds[24];
							}
						} else {
							if (values[6] <= thresholds[7]) {
								result += thresholds[20];
							} else {
								result += thresholds[22];
							}
						}
					}
				}
				// tree 1 ...
				if (values[1] <= thresholds[28]) {
					if (values[1] <= thresholds[1]) {
						if (values[1] <= thresholds[36]) {
							if (values[45] <= thresholds[4]) {
								result += thresholds[37];
							} else {
								result += thresholds[52];
							}
						} else {
							if (values[20] <= thresholds[4]) {
								result += thresholds[50];
							} else {
								result += thresholds[51];
							}
						}
					} else {
						if (values[1] <= thresholds[29]) {
							if (values[16] <= thresholds[4]) {
								result += thresholds[39];
							} else {
								result += thresholds[42];
							}
						} else {
							if (values[4] <= thresholds[32]) {
								result += thresholds[40];
							} else {
								result += thresholds[46];
							}
						}
					}
				} else {
					if (values[1] <= thresholds[30]) {
						if (values[6] <= thresholds[31]) {
							if (values[46] <= thresholds[4]) {
								result += thresholds[38];
							} else {
								result += thresholds[44];
							}
						} else {
							if (values[10] <= thresholds[34]) {
								result += thresholds[43];
							} else {
								result += thresholds[48];
							}
						}
					} else {
						if (values[43] <= thresholds[4]) {
							if (values[1] <= thresholds[35]) {
								result += thresholds[41];
							} else {
								result += thresholds[49];
							}
						} else {
							if (values[10] <= thresholds[33]) {
								result += thresholds[45];
							} else {
								result += thresholds[47];
							}
						}
					}
				}
				// tree 2 ...
				if (values[1] <= thresholds[53]) {
					if (values[1] <= thresholds[1]) {
						if (values[1] <= thresholds[10]) {
							if (values[6] <= thresholds[61]) {
								result += thresholds[62];
							} else {
								result += thresholds[77];
							}
						} else {
							if (values[4] <= thresholds[60]) {
								result += thresholds[74];
							} else {
								result += thresholds[75];
							}
						}
					} else {
						if (values[1] <= thresholds[54]) {
							if (values[26] <= thresholds[4]) {
								result += thresholds[64];
							} else {
								result += thresholds[67];
							}
						} else {
							if (values[4] <= thresholds[58]) {
								result += thresholds[65];
							} else {
								result += thresholds[71];
							}
						}
					}
				} else {
					if (values[1] <= thresholds[55]) {
						if (values[10] <= thresholds[56]) {
							if (values[4] <= thresholds[57]) {
								result += thresholds[63];
							} else {
								result += thresholds[69];
							}
						} else {
							if (values[47] <= thresholds[4]) {
								result += thresholds[68];
							} else {
								result += thresholds[76];
							}
						}
					} else {
						if (values[43] <= thresholds[4]) {
							if (values[1] <= thresholds[59]) {
								result += thresholds[66];
							} else {
								result += thresholds[73];
							}
						} else {
							if (values[6] <= thresholds[7]) {
								result += thresholds[70];
							} else {
								result += thresholds[72];
							}
						}
					}
				}
				// tree 3 ...
				if (values[1] <= thresholds[78]) {
					if (values[1] <= thresholds[1]) {
						if (values[1] <= thresholds[10]) {
							if (values[6] <= thresholds[61]) {
								result += thresholds[86];
							} else {
								result += thresholds[101];
							}
						} else {
							if (values[4] <= thresholds[85]) {
								result += thresholds[99];
							} else {
								result += thresholds[100];
							}
						}
					} else {
						if (values[37] <= thresholds[4]) {
							if (values[36] <= thresholds[4]) {
								result += thresholds[88];
							} else {
								result += thresholds[91];
							}
						} else {
							if (values[1] <= thresholds[80]) {
								result += thresholds[90];
							} else {
								result += thresholds[93];
							}
						}
					}
				} else {
					if (values[1] <= thresholds[55]) {
						if (values[8] <= thresholds[79]) {
							if (values[10] <= thresholds[81]) {
								result += thresholds[87];
							} else {
								result += thresholds[95];
							}
						} else {
							if (values[6] <= thresholds[83]) {
								result += thresholds[92];
							} else {
								result += thresholds[97];
							}
						}
					} else {
						if (values[43] <= thresholds[4]) {
							if (values[1] <= thresholds[84]) {
								result += thresholds[89];
							} else {
								result += thresholds[98];
							}
						} else {
							if (values[6] <= thresholds[82]) {
								result += thresholds[94];
							} else {
								result += thresholds[96];
							}
						}
					}
				}
				// tree 4 ...
				if (values[1] <= thresholds[102]) {
					if (values[1] <= thresholds[1]) {
						if (values[1] <= thresholds[36]) {
							if (values[13] <= thresholds[4]) {
								result += thresholds[107];
							} else {
								result += thresholds[120];
							}
						} else {
							if (values[11] <= thresholds[4]) {
								result += thresholds[117];
							} else {
								result += thresholds[119];
							}
						}
					} else {
						if (values[37] <= thresholds[4]) {
							if (values[36] <= thresholds[4]) {
								result += thresholds[109];
							} else {
								result += thresholds[111];
							}
						} else {
							if (values[1] <= thresholds[104]) {
								result += thresholds[110];
							} else {
								result += thresholds[115];
							}
						}
					}
				} else {
					if (values[1] <= thresholds[9]) {
						if (values[4] <= thresholds[60]) {
							if (values[46] <= thresholds[4]) {
								result += thresholds[108];
							} else {
								result += thresholds[116];
							}
						} else {
							if (values[8] <= thresholds[103]) {
								result += thresholds[113];
							} else {
								result += thresholds[114];
							}
						}
					} else {
						if (values[41] <= thresholds[4]) {
							if (values[1] <= thresholds[105]) {
								result += thresholds[112];
							} else {
								result += thresholds[121];
							}
						} else {
							if (values[10] <= thresholds[106]) {
								result += thresholds[118];
							} else {
								result += thresholds[122];
							}
						}
					}
				}
				// tree 5 ...
				if (values[1] <= thresholds[123]) {
					if (values[1] <= thresholds[124]) {
						if (values[11] <= thresholds[4]) {
							if (values[1] <= thresholds[10]) {
								result += thresholds[133];
							} else {
								result += thresholds[147];
							}
						} else {
							if (values[10] <= thresholds[132]) {
								result += thresholds[144];
							} else {
								result += thresholds[148];
							}
						}
					} else {
						if (values[26] <= thresholds[4]) {
							if (values[4] <= thresholds[126]) {
								result += thresholds[135];
							} else {
								result += thresholds[138];
							}
						} else {
							if (values[10] <= thresholds[131]) {
								result += thresholds[137];
							} else {
								result += thresholds[146];
							}
						}
					}
				} else {
					if (values[1] <= thresholds[125]) {
						if (values[6] <= thresholds[127]) {
							if (values[46] <= thresholds[4]) {
								result += thresholds[134];
							} else {
								result += thresholds[140];
							}
						} else {
							if (values[10] <= thresholds[128]) {
								result += thresholds[139];
							} else {
								result += thresholds[142];
							}
						}
					} else {
						if (values[43] <= thresholds[4]) {
							if (values[6] <= thresholds[130]) {
								result += thresholds[136];
							} else {
								result += thresholds[145];
							}
						} else {
							if (values[10] <= thresholds[129]) {
								result += thresholds[141];
							} else {
								result += thresholds[143];
							}
						}
					}
				}
				// tree 6 ...
				if (values[1] <= thresholds[149]) {
					if (values[1] <= thresholds[150]) {
						if (values[45] <= thresholds[4]) {
							if (values[24] <= thresholds[4]) {
								result += thresholds[157];
							} else {
								result += thresholds[169];
							}
						} else {
							if (values[1] <= thresholds[36]) {
								result += thresholds[168];
							} else {
								result += thresholds[172];
							}
						}
					} else {
						if (values[1] <= thresholds[151]) {
							if (values[18] <= thresholds[4]) {
								result += thresholds[159];
							} else {
								result += thresholds[161];
							}
						} else {
							if (values[4] <= thresholds[152]) {
								result += thresholds[160];
							} else {
								result += thresholds[162];
							}
						}
					}
				} else {
					if (values[1] <= thresholds[153]) {
						if (values[4] <= thresholds[154]) {
							if (values[6] <= thresholds[156]) {
								result += thresholds[158];
							} else {
								result += thresholds[166];
							}
						} else {
							if (values[8] <= thresholds[155]) {
								result += thresholds[164];
							} else {
								result += thresholds[165];
							}
						}
					} else {
						if (values[41] <= thresholds[4]) {
							if (values[1] <= thresholds[105]) {
								result += thresholds[163];
							} else {
								result += thresholds[170];
							}
						} else {
							if (values[10] <= thresholds[106]) {
								result += thresholds[167];
							} else {
								result += thresholds[171];
							}
						}
					}
				}
				// tree 7 ...
				if (values[1] <= thresholds[173]) {
					if (values[1] <= thresholds[150]) {
						if (values[45] <= thresholds[4]) {
							if (values[47] <= thresholds[4]) {
								result += thresholds[180];
							} else {
								result += thresholds[194];
							}
						} else {
							if (values[1] <= thresholds[36]) {
								result += thresholds[193];
							} else {
								result += thresholds[195];
							}
						}
					} else {
						if (values[1] <= thresholds[174]) {
							if (values[16] <= thresholds[4]) {
								result += thresholds[182];
							} else {
								result += thresholds[184];
							}
						} else {
							if (values[8] <= thresholds[175]) {
								result += thresholds[183];
							} else {
								result += thresholds[185];
							}
						}
					}
				} else {
					if (values[6] <= thresholds[156]) {
						if (values[6] <= thresholds[177]) {
							if (values[4] <= thresholds[178]) {
								result += thresholds[181];
							} else {
								result += thresholds[191];
							}
						} else {
							if (values[46] <= thresholds[4]) {
								result += thresholds[188];
							} else {
								result += thresholds[189];
							}
						}
					} else {
						if (values[10] <= thresholds[176]) {
							if (values[10] <= thresholds[179]) {
								result += thresholds[186];
							} else {
								result += thresholds[192];
							}
						} else {
							if (values[11] <= thresholds[4]) {
								result += thresholds[187];
							} else {
								result += thresholds[190];
							}
						}
					}
				}
				// tree 8 ...
				if (values[1] <= thresholds[196]) {
					if (values[1] <= thresholds[124]) {
						if (values[11] <= thresholds[4]) {
							if (values[1] <= thresholds[10]) {
								result += thresholds[203];
							} else {
								result += thresholds[215];
							}
						} else {
							if (values[10] <= thresholds[132]) {
								result += thresholds[213];
							} else {
								result += thresholds[216];
							}
						}
					} else {
						if (values[1] <= thresholds[197]) {
							if (values[11] <= thresholds[4]) {
								result += thresholds[205];
							} else {
								result += thresholds[207];
							}
						} else {
							if (values[4] <= thresholds[58]) {
								result += thresholds[206];
							} else {
								result += thresholds[208];
							}
						}
					}
				} else {
					if (values[1] <= thresholds[35]) {
						if (values[8] <= thresholds[198]) {
							if (values[6] <= thresholds[200]) {
								result += thresholds[204];
							} else {
								result += thresholds[212];
							}
						} else {
							if (values[4] <= thresholds[199]) {
								result += thresholds[210];
							} else {
								result += thresholds[211];
							}
						}
					} else {
						if (values[41] <= thresholds[4]) {
							if (values[1] <= thresholds[201]) {
								result += thresholds[209];
							} else {
								result += thresholds[217];
							}
						} else {
							if (values[1] <= thresholds[202]) {
								result += thresholds[214];
							} else {
								result += thresholds[218];
							}
						}
					}
				}
				// tree 9 ...
				if (values[1] <= thresholds[219]) {
					if (values[1] <= thresholds[124]) {
						if (values[11] <= thresholds[4]) {
							if (values[1] <= thresholds[10]) {
								result += thresholds[225];
							} else {
								result += thresholds[239];
							}
						} else {
							if (values[10] <= thresholds[132]) {
								result += thresholds[237];
							} else {
								result += thresholds[240];
							}
						}
					} else {
						if (values[4] <= thresholds[220]) {
							if (values[10] <= thresholds[222]) {
								result += thresholds[227];
							} else {
								result += thresholds[233];
							}
						} else {
							if (values[16] <= thresholds[4]) {
								result += thresholds[228];
							} else {
								result += thresholds[230];
							}
						}
					}
				} else {
					if (values[1] <= thresholds[221]) {
						if (values[10] <= thresholds[56]) {
							if (values[4] <= thresholds[85]) {
								result += thresholds[226];
							} else {
								result += thresholds[232];
							}
						} else {
							if (values[6] <= thresholds[224]) {
								result += thresholds[231];
							} else {
								result += thresholds[236];
							}
						}
					} else {
						if (values[43] <= thresholds[4]) {
							if (values[41] <= thresholds[4]) {
								result += thresholds[229];
							} else {
								result += thresholds[238];
							}
						} else {
							if (values[10] <= thresholds[223]) {
								result += thresholds[234];
							} else {
								result += thresholds[235];
							}
						}
					}
				}
				// tree 10 ...
				if (values[1] <= thresholds[241]) {
					if (values[1] <= thresholds[150]) {
						if (values[13] <= thresholds[4]) {
							if (values[24] <= thresholds[4]) {
								result += thresholds[247];
							} else {
								result += thresholds[260];
							}
						} else {
							if (values[2] <= thresholds[245]) {
								result += thresholds[258];
							} else {
								result += thresholds[259];
							}
						}
					} else {
						if (values[37] <= thresholds[4]) {
							if (values[26] <= thresholds[4]) {
								result += thresholds[249];
							} else {
								result += thresholds[251];
							}
						} else {
							if (values[1] <= thresholds[242]) {
								result += thresholds[250];
							} else {
								result += thresholds[253];
							}
						}
					}
				} else {
					if (values[1] <= thresholds[35]) {
						if (values[8] <= thresholds[243]) {
							if (values[6] <= thresholds[200]) {
								result += thresholds[248];
							} else {
								result += thresholds[256];
							}
						} else {
							if (values[4] <= thresholds[244]) {
								result += thresholds[254];
							} else {
								result += thresholds[255];
							}
						}
					} else {
						if (values[41] <= thresholds[4]) {
							if (values[1] <= thresholds[246]) {
								result += thresholds[252];
							} else {
								result += thresholds[261];
							}
						} else {
							if (values[10] <= thresholds[106]) {
								result += thresholds[257];
							} else {
								result += thresholds[262];
							}
						}
					}
				}
				// tree 11 ...
				if (values[1] <= thresholds[263]) {
					if (values[1] <= thresholds[124]) {
						if (values[11] <= thresholds[4]) {
							if (values[1] <= thresholds[267]) {
								result += thresholds[268];
							} else {
								result += thresholds[279];
							}
						} else {
							if (values[10] <= thresholds[132]) {
								result += thresholds[278];
							} else {
								result += thresholds[281];
							}
						}
					} else {
						if (values[18] <= thresholds[4]) {
							if (values[4] <= thresholds[126]) {
								result += thresholds[270];
							} else {
								result += thresholds[272];
							}
						} else {
							if (values[1] <= thresholds[265]) {
								result += thresholds[271];
							} else {
								result += thresholds[276];
							}
						}
					}
				} else {
					if (values[1] <= thresholds[9]) {
						if (values[46] <= thresholds[4]) {
							if (values[6] <= thresholds[264]) {
								result += thresholds[269];
							} else {
								result += thresholds[275];
							}
						} else {
							if (values[10] <= thresholds[266]) {
								result += thresholds[274];
							} else {
								result += thresholds[277];
							}
						}
					} else {
						if (values[41] <= thresholds[4]) {
							if (values[1] <= thresholds[105]) {
								result += thresholds[273];
							} else {
								result += thresholds[282];
							}
						} else {
							if (values[1] <= thresholds[202]) {
								result += thresholds[280];
							} else {
								result += thresholds[283];
							}
						}
					}
				}
				// tree 12 ...
				if (values[1] <= thresholds[241]) {
					if (values[1] <= thresholds[150]) {
						if (values[1] <= thresholds[267]) {
							if (values[6] <= thresholds[286]) {
								result += thresholds[288];
							} else {
								result += thresholds[301];
							}
						} else {
							if (values[4] <= thresholds[60]) {
								result += thresholds[298];
							} else {
								result += thresholds[299];
							}
						}
					} else {
						if (values[37] <= thresholds[4]) {
							if (values[26] <= thresholds[4]) {
								result += thresholds[290];
							} else {
								result += thresholds[292];
							}
						} else {
							if (values[1] <= thresholds[284]) {
								result += thresholds[291];
							} else {
								result += thresholds[294];
							}
						}
					}
				} else {
					if (values[1] <= thresholds[35]) {
						if (values[4] <= thresholds[58]) {
							if (values[6] <= thresholds[82]) {
								result += thresholds[289];
							} else {
								result += thresholds[297];
							}
						} else {
							if (values[8] <= thresholds[285]) {
								result += thresholds[295];
							} else {
								result += thresholds[296];
							}
						}
					} else {
						if (values[41] <= thresholds[4]) {
							if (values[1] <= thresholds[201]) {
								result += thresholds[293];
							} else {
								result += thresholds[302];
							}
						} else {
							if (values[6] <= thresholds[287]) {
								result += thresholds[300];
							} else {
								result += thresholds[303];
							}
						}
					}
				}
				// tree 13 ...
				if (values[1] <= thresholds[304]) {
					if (values[14] <= thresholds[4]) {
						if (values[18] <= thresholds[4]) {
							if (values[16] <= thresholds[4]) {
								result += thresholds[310];
							} else {
								result += thresholds[314];
							}
						} else {
							if (values[1] <= thresholds[307]) {
								result += thresholds[313];
							} else {
								result += thresholds[319];
							}
						}
					} else {
						if (values[1] <= thresholds[36]) {
							if (values[6] <= thresholds[309]) {
								result += thresholds[312];
							} else {
								result += thresholds[324];
							}
						} else {
							if (values[10] <= thresholds[308]) {
								result += thresholds[320];
							} else {
								result += thresholds[321];
							}
						}
					}
				} else {
					if (values[1] <= thresholds[59]) {
						if (values[8] <= thresholds[305]) {
							if (values[10] <= thresholds[306]) {
								result += thresholds[311];
							} else {
								result += thresholds[317];
							}
						} else {
							if (values[6] <= thresholds[83]) {
								result += thresholds[316];
							} else {
								result += thresholds[318];
							}
						}
					} else {
						if (values[41] <= thresholds[4]) {
							if (values[1] <= thresholds[105]) {
								result += thresholds[315];
							} else {
								result += thresholds[323];
							}
						} else {
							if (values[10] <= thresholds[106]) {
								result += thresholds[322];
							} else {
								result += thresholds[325];
							}
						}
					}
				}
				// tree 14 ...
				if (values[1] <= thresholds[326]) {
					if (values[14] <= thresholds[4]) {
						if (values[1] <= thresholds[327]) {
							if (values[11] <= thresholds[4]) {
								result += thresholds[333];
							} else {
								result += thresholds[337];
							}
						} else {
							if (values[4] <= thresholds[328]) {
								result += thresholds[336];
							} else {
								result += thresholds[338];
							}
						}
					} else {
						if (values[1] <= thresholds[36]) {
							if (values[6] <= thresholds[332]) {
								result += thresholds[335];
							} else {
								result += thresholds[348];
							}
						} else {
							if (values[10] <= thresholds[308]) {
								result += thresholds[346];
							} else {
								result += thresholds[347];
							}
						}
					}
				} else {
					if (values[43] <= thresholds[4]) {
						if (values[46] <= thresholds[4]) {
							if (values[41] <= thresholds[4]) {
								result += thresholds[334];
							} else {
								result += thresholds[345];
							}
						} else {
							if (values[6] <= thresholds[329]) {
								result += thresholds[340];
							} else {
								result += thresholds[341];
							}
						}
					} else {
						if (values[10] <= thresholds[330]) {
							if (values[1] <= thresholds[331]) {
								result += thresholds[339];
							} else {
								result += thresholds[344];
							}
						} else {
							if (values[6] <= thresholds[264]) {
								result += thresholds[342];
							} else {
								result += thresholds[343];
							}
						}
					}
				}
				// tree 15 ...
				if (values[1] <= thresholds[349]) {
					if (values[1] <= thresholds[36]) {
						if (values[13] <= thresholds[4]) {
							if (values[24] <= thresholds[4]) {
								result += thresholds[353];
							} else {
								result += thresholds[366];
							}
						} else {
							if (values[2] <= thresholds[245]) {
								result += thresholds[363];
							} else {
								result += thresholds[364];
							}
						}
					} else {
						if (values[37] <= thresholds[4]) {
							if (values[36] <= thresholds[4]) {
								result += thresholds[355];
							} else {
								result += thresholds[357];
							}
						} else {
							if (values[1] <= thresholds[350]) {
								result += thresholds[356];
							} else {
								result += thresholds[360];
							}
						}
					}
				} else {
					if (values[1] <= thresholds[35]) {
						if (values[4] <= thresholds[58]) {
							if (values[38] <= thresholds[4]) {
								result += thresholds[354];
							} else {
								result += thresholds[362];
							}
						} else {
							if (values[8] <= thresholds[351]) {
								result += thresholds[359];
							} else {
								result += thresholds[361];
							}
						}
					} else {
						if (values[41] <= thresholds[4]) {
							if (values[5] <= thresholds[352]) {
								result += thresholds[358];
							} else {
								result += thresholds[367];
							}
						} else {
							if (values[6] <= thresholds[287]) {
								result += thresholds[365];
							} else {
								result += thresholds[368];
							}
						}
					}
				}
				// tree 16 ...
				if (values[1] <= thresholds[369]) {
					if (values[14] <= thresholds[4]) {
						if (values[4] <= thresholds[370]) {
							if (values[1] <= thresholds[371]) {
								result += thresholds[376];
							} else {
								result += thresholds[381];
							}
						} else {
							if (values[16] <= thresholds[4]) {
								result += thresholds[379];
							} else {
								result += thresholds[380];
							}
						}
					} else {
						if (values[1] <= thresholds[10]) {
							if (values[6] <= thresholds[11]) {
								result += thresholds[378];
							} else {
								result += thresholds[387];
							}
						} else {
							if (values[4] <= thresholds[374]) {
								result += thresholds[385];
							} else {
								result += thresholds[386];
							}
						}
					}
				} else {
					if (values[1] <= thresholds[35]) {
						if (values[10] <= thresholds[372]) {
							if (values[4] <= thresholds[373]) {
								result += thresholds[377];
							} else {
								result += thresholds[384];
							}
						} else {
							if (values[5] <= thresholds[375]) {
								result += thresholds[383];
							} else {
								result += thresholds[389];
							}
						}
					} else {
						if (values[41] <= thresholds[4]) {
							if (values[1] <= thresholds[201]) {
								result += thresholds[382];
							} else {
								result += thresholds[390];
							}
						} else {
							if (values[10] <= thresholds[106]) {
								result += thresholds[388];
							} else {
								result += thresholds[391];
							}
						}
					}
				}
				// tree 17 ...
				if (values[1] <= thresholds[174]) {
					if (values[1] <= thresholds[392]) {
						if (values[11] <= thresholds[4]) {
							if (values[24] <= thresholds[4]) {
								result += thresholds[400];
							} else {
								result += thresholds[411];
							}
						} else {
							if (values[10] <= thresholds[132]) {
								result += thresholds[409];
							} else {
								result += thresholds[412];
							}
						}
					} else {
						if (values[6] <= thresholds[332]) {
							if (values[9] <= thresholds[394]) {
								result += thresholds[402];
							} else {
								result += thresholds[405];
							}
						} else {
							if (values[4] <= thresholds[393]) {
								result += thresholds[403];
							} else {
								result += thresholds[404];
							}
						}
					}
				} else {
					if (values[10] <= thresholds[395]) {
						if (values[1] <= thresholds[59]) {
							if (values[8] <= thresholds[396]) {
								result += thresholds[401];
							} else {
								result += thresholds[408];
							}
						} else {
							if (values[1] <= thresholds[105]) {
								result += thresholds[407];
							} else {
								result += thresholds[414];
							}
						}
					} else {
						if (values[6] <= thresholds[397]) {
							if (values[10] <= thresholds[398]) {
								result += thresholds[406];
							} else {
								result += thresholds[413];
							}
						} else {
							if (values[10] <= thresholds[399]) {
								result += thresholds[410];
							} else {
								result += thresholds[415];
							}
						}
					}
				}
				// tree 18 ...
				if (values[1] <= thresholds[55]) {
					if (values[26] <= thresholds[4]) {
						if (values[1] <= thresholds[10]) {
							if (values[6] <= thresholds[61]) {
								result += thresholds[419];
							} else {
								result += thresholds[434];
							}
						} else {
							if (values[4] <= thresholds[370]) {
								result += thresholds[422];
							} else {
								result += thresholds[423];
							}
						}
					} else {
						if (values[10] <= thresholds[131]) {
							if (values[6] <= thresholds[418]) {
								result += thresholds[421];
							} else {
								result += thresholds[433];
							}
						} else {
							if (values[5] <= thresholds[417]) {
								result += thresholds[430];
							} else {
								result += thresholds[432];
							}
						}
					}
				} else {
					if (values[43] <= thresholds[4]) {
						if (values[46] <= thresholds[4]) {
							if (values[38] <= thresholds[4]) {
								result += thresholds[420];
							} else {
								result += thresholds[429];
							}
						} else {
							if (values[6] <= thresholds[329]) {
								result += thresholds[427];
							} else {
								result += thresholds[428];
							}
						}
					} else {
						if (values[10] <= thresholds[129]) {
							if (values[6] <= thresholds[416]) {
								result += thresholds[424];
							} else {
								result += thresholds[431];
							}
						} else {
							if (values[6] <= thresholds[127]) {
								result += thresholds[425];
							} else {
								result += thresholds[426];
							}
						}
					}
				}
				// tree 19 ...
				if (values[26] <= thresholds[4]) {
					if (values[1] <= thresholds[435]) {
						if (values[1] <= thresholds[10]) {
							if (values[6] <= thresholds[61]) {
								result += thresholds[443];
							} else {
								result += thresholds[453];
							}
						} else {
							if (values[6] <= thresholds[436]) {
								result += thresholds[446];
							} else {
								result += thresholds[447];
							}
						}
					} else {
						if (values[43] <= thresholds[4]) {
							if (values[6] <= thresholds[130]) {
								result += thresholds[445];
							} else {
								result += thresholds[450];
							}
						} else {
							if (values[10] <= thresholds[223]) {
								result += thresholds[448];
							} else {
								result += thresholds[449];
							}
						}
					}
				} else {
					if (values[10] <= thresholds[437]) {
						if (values[6] <= thresholds[438]) {
							if (values[6] <= thresholds[439]) {
								result += thresholds[444];
							} else {
								result += thresholds[454];
							}
						} else {
							if (values[1] <= thresholds[327]) {
								result += thresholds[452];
							} else {
								result += thresholds[457];
							}
						}
					} else {
						if (values[1] <= thresholds[440]) {
							if (values[7] <= thresholds[441]) {
								result += thresholds[451];
							} else {
								result += thresholds[456];
							}
						} else {
							if (values[4] <= thresholds[442]) {
								result += thresholds[455];
							} else {
								result += thresholds[458];
							}
						}
					}
				}
			return 1.0f / (1.0f + exp(-1.0 * result));
		}
	};
}

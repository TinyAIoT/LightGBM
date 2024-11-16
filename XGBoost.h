#pragma once
namespace LightGBM { 
		class CovTypeClassifier {
		public:
			float predict(const float values[17]) {
				float result = 0;
				float thresholds[123];
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
				int features[17];
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
			return 1.0f / (1.0f + exp(-1.0 * result));
		}
	};
}

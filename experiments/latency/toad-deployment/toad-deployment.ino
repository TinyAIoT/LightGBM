#define SUCCESS 0
#define ERROR_INVALID_ARGUMENT -1
#define ERROR_INVALID_INPUT -2
#define ERROR_FAILED_READ -3
#define ERROR_OUT_OF_MEMORY -4
#define DEBUG true
#define DEBUGold false
#define BITS_PER_BYTE 8ul
#define BUFFER_SIZE 1024ul
unsigned char gpBuffer[BUFFER_SIZE];
char endMarker = '\n';
int incomingData = 0;
// F1		   f2		   f3
byte featurecharac[] = {19, 83, 39, 82, 103, 34, 146, 11, 32, 210, 0};
// TODO we could also represent this as a unsigned int/long to haveless reading operations?
// 000 100 1 1.0101 --> 1
// 001 1.00 1 00111 --> 4
// 010 100 1 0.0110 --> 6
// 011 1.00 1 00010 --> 8
// 100 100 1 0.0001 --> 10
// 101 1.00 1 00001 --> 16
// 110 100 1 00001 --> 18
// 111 leave (1) 
// global Features & Threholds
float features[] = {3078.5, 2505.5, 2451.5, 2414.5, 2488.5, 3014.5, 3296.5, 3161.5, 3350.5, 3396.5,
                    3087.5, 2434.5, 2223.5, 3021.5, 3365.5, 3099.5, 3027.5, 3299.5, 3360.5, 2991.5, 
                    2681.5, 3194.5,
// 4
477, 307.5, 552.5, 181, 166, 205.5, 360.5, 214, 
// 6
702.5, 1103.5, 1350.5, 1167.5, 658.5, 5440.5, 4951.5,
// 8
238.5, 239.5, 241.5,
// 10 
2045.5,
// 16 
0,
//18
0};
// 1 16 4 8 18 

// Tree 0
byte tree0[] = {0,1,6,2,5, 48, 32, 12, 18, 128, 128, 28, 132, 136, 36,
// 96,7,4,5,160,32,8,33,34,9, beforehand 3,96, 112, 64, 90, 32, 32, 146, 130, 64,
                0,14,9,13,2,6,4,10,1,
                8,5,7,3,12,11,15};
// 000 00000 // 000 00001 // 000 00010 // 000 00011 // 000 00100 // 000 00101 // 101 00000 // 001 00000 // 000 00110 // 011 00000 // 000 00111  // 001 00010  // 000 01000 // 001 00010 // 000 01001
// 1 0       // 1 1       // 1 2       // 1 3       // 1 4       // 1 5       // 16 0      // 4 0       // 1 6       // 8 0       // 1 7        // 4 2        // 1 8       // 4 2       // 1 9
// 1 0       // 1 1       // 1 6       // 1 2       // 1 3       // 8 0       // 1 7        // 1 4        // 1 5       // 16 0     // 4 0        // 1 8       // 4 1        // 4 2       // 1 9
// 000 00000 // 000 00001 // 000 00110 // 000 00010 // 000 00011 // 011 0     // 000 00111  // 000 00100 // 000 00101 // 101 0     // 001 000    // 000 01000 // 001 001   // 001 010 // 000 01001
// 1 -> 0    // 1 -> 1    // 1 -> 6     // 1 -> 2    // 1 -> 5   // 8 -> 0 // 1 -> 8    // 1 -> 3    // 1 -> 4    // 16 -> 0   // 4 -> 0.   // 1 -> 7    // 4 -> 1   // 4 -> 2    // 1 -> 9
// 000 00000 // 000 00001 // 000 00110 // 000 00010 // 000 00101 // 011 00 // 000 01000 // 000 00011 // 000 00100 // 101 00000 // 001 00000 // 000 00111 // 001 00001 // 001 00010 // 000 01001

byte tree1[] = {10,1,6,11,13, 52, 32, 48, 188, 112, 211, 138, 14,
// 97,8,11,36,80,37,38,39,34,13, \\ Leaves starting  104, 64, 89, 232, 195, 78, 40, 56,
                16,31,26,29,18,21,19,24,17,25,
                22,23,20,28,27,30};
// 1 -> 10 // 1 -> 1 // 1 -> 11 // 1 -> 12 // 4 -> 3 // 1 -> 13 // 16 -> 0 // 4 -> 4 
            // 1 -> 6 // 8 -> 1 // 4 -> 5 // 4 -> 5 // 1 -> 8 // 4 -> 3 // 1 -> 14
// 1 -> 10   // 1 -> 1    // 1 -> 6     // 1 -> 11 // 1 -> 12  // 8 -> 1      // 1 -> 8         // 1 -> 11.   // 4 -> 3   // 16 -> 0  // 4 -> 4  // 4 -> 5  // 4 -> 6  // 4 -> 2  // 1 -> 13.
// 000 01010 // 000 00001 // 000 00110 // 000 01011 // 000 01100// 011 01     // 000. 01000 //  000 01011 // 001 011   // 101 0.   // 001 100 //001 101  // 001 110 // 001 010 // 000 01110
// 1 -> 10 // 1 -> 1      // 1 -> 6     // 1 -> 11  // 1 -> 13    // 4 -> 1     // 1 -> 8       // 1 -> 12   // 2 -> 3 // 6 -> 1 // 2 -> 4  // 2 -> 5   // 2 -> 6 // 2 -> 2 // 1 -> 14
// 000 01010 // 000 00001 // 000 00110 // 000 01011 // 000 1101  // 011 -> 01 // 000 -> 01000 // 000 01100 // 001 011 // 110 0 // 011 100  // 001 101  // 001 110 // 001 010 // 000 01110
byte tree2[] = {15,1,16,2,17,96, 146, 25, 134, 34, 122, 73, 128,
// 96,18,64,192,192,36,65,39,66,67,
                32,46,42,45,34,37,35,40,33,41,
                38,39,36,44,43,47};
// 1 15 // 1 1 // 1 2 // 6 0 // 18 0 // 1 16 // 18 0 // 4 4 // 1 17 // 8 0 // 6 1 // 4 7 // 1 18 // 6 2 // 6 3
// 1 15       // 1 1       // 1 16      // 1 2       //  1 17     // 8 0  // 1 18      // 6 0     // 18 0  // 18 0 // 4 4    // 6 1     // 4 7     // 6 2   // 6 3
// 000 01111 // 000 00001 // 000 10000 // 000 00010 // 000 10001 // 011 00 // 000 10010 // 010 000 // 110 0 // 110 0 // 001 100 // 010 001 // 001 111 // 010 010 // 010 011
byte tree3[] = {0,4,21,11, 199, 34, 161, 98, 98, 33, 1, 171, 11, 0,
//192,98,65,68,35,19,20,35,69,128,71,
// 98 98 33 1 171 11 0
                48,63,61,62,50,53,52,56,49,57,
                54,59,51,60,55,58};
// 1 0 // 1 4 // 1 11 // 6 4 // 4 3 // 18 0 // 1 19 // 1 20 // 1 21 // 8 2 // 4 3 // 6 5 // 6 1 // 10 0 // 6 6
// 1 0        // 1 4      // 1 21      // 1 11      // 18 0  // 8 2    // 6 1    // 6 4      // 4 3       // 1 19         // 1 20       // 4 3      // 6 5     // 10 0      // 6 6
// 000 00000 // 000 00100 // 000 10101 // 000 01011 // 110 0 // 011 1.0 // 010 001 // 0.10 100 // 001. 011 // 000 1.0011 // 000 1.0100 // 001 .011 // 010 10.1 // 100 0 // 010 110
                                                    // 11000111 00100010 10100001 01100010 01100010 100 00101 10101011 00000000 10110000
                                                    // 11000111 00100010101000010110001001    10001010000101101010110000000010110000

float leaf_values[] = {-0.23497,-0.117087,0.0503431,-0.206828,-0.0493795,-0.112627,-0.174697,0.00136021,-0.161709,-0.168538,// (9)
                      0.0499784,-0.225998,-0.14403,-0.104267,-0.203637,-0.24182,-0.176645,-0.117526,0.0889293,-0.0395473,
                      -0.143167,-0.113582,-0.0509038,0.0566713,0.038456,-0.0661403,-0.0725426,-0.152461,-0.0855609,-0.134016,
                      -0.171829,-0.163127,-0.143196,-0.0173605,0.0818071,-0.0451547,-0.0738508,-0.0746999,-0.0785135,0.0224879,
                      0.0293355,-0.096912,-0.0621734,-0.128676,-0.138808,-0.160606,-0.163553,-0.161702,-0.135517,-0.091976, // 49
                      0.0783967,-0.082263,-0.167573,0.0230662,0.0224351,-0.120759,0.0456806,-0.0298806,-0.0494573,0.168141,
                      0.0707365,-0.0693165,-0.135754,-0.154731}; // 64
// global leaf values
// 000 100 1 10101 --> 1
// 001 100 1 00111 --> 4
// 010 100 1 00110 --> 6
// 011 100 1 00010 --> 8
// 100 100 1 00001 --> 10
// 101 100 1 00001 --> 16
// 110 100 1 00001 --> 18
struct Feature
{
    byte tindex;
    byte refsize;
    byte size; // 0 = 1 1
    bool type; // 0->int 1->float
    byte nthres;
   Feature(){
   }
   Feature(const byte ptindex, const byte psize, const bool ptype, byte pnthres) : tindex(ptindex), size(psize), type(ptype), nthres(pnthres)
   {
    if (pnthres == 0 || pnthres == 1) {
      refsize = 1;
    } else {
      pnthres = pnthres - 1;
      byte bits = 0;
      while (pnthres) { ++bits; pnthres >>= 1; }
      refsize = bits;
    }
   }
};
int parseInput(size_t& bufferSize, unsigned char* pBuffer) {
  int input;
  if (pBuffer == nullptr)
    return ERROR_INVALID_ARGUMENT;
  for (size_t bitIndex = 0ul; bitIndex / BITS_PER_BYTE < bufferSize; ++bitIndex) {
    input = Serial.read();
    switch (input) {
      case '0':
        bitSet(pBuffer[bitIndex / BITS_PER_BYTE], bitIndex % BITS_PER_BYTE);
        break;
      case '1':
        bitClear(pBuffer[bitIndex / BITS_PER_BYTE], bitIndex % BITS_PER_BYTE);
        break;
      case ' ':
      case '\t':
      case '\r':
        break;
      case '\n':
        bufferSize = bitIndex / BITS_PER_BYTE;
        return SUCCESS;
      case -1:
        return ERROR_FAILED_READ;
      default:
        return ERROR_INVALID_INPUT;
    }
  }
  return ERROR_OUT_OF_MEMORY;
}
template<typename T>
Print& operator<<(Print& printer, T value) {
  printer.print(value);
  return printer;
}
byte checkifoneortwoBytes(byte number, byte number2, byte offset, byte offset2) {
  byte size;
  if ((8-offset < 0) & (8-offset2 < 0)) {
    size = bytetobyterange(number2, offset, offset2);
  } else if (8-offset-6 < 0){
    size = getBitsfromTwoBytes(number, number2, 8-offset, 8 + (offset2));
  } else {
    size = bytetobyterange(number, offset, offset2);
  }
  return size;
}
byte bytetobyterange(byte toextract, byte start, byte end) {
  // start = 8 end = 6
  // 11111111 -> 00000011
  // start = 5 end = 3
  // 11111111 -> 00000011
  // start = 8 end = 6
  // 11111111 -> 00000011
  if (start < end) {
    // Serial << "bytetobyterange was called with start (" << start << ") smaller than end (" << end << ") - ABORT";
    return 0;
  }
  byte newbyte = 0;
  newbyte = (toextract >> (end));
  // 00000101 << 7 = 10000000
  newbyte = (newbyte << (8 - start + end));
  // 10000000 >> 7 = 00000001
  newbyte = (newbyte >> (8 - start + end));
  return newbyte;
}

// arrays are passed by reference as default
float evaltree(byte tree[], float input[], Feature featurecollection[]) {
  byte node = 0;
  byte previousnode = 0;
  byte offsets[] = {0,0,0,0,0,0};
  byte localoffsets[] = {0,0,0,0,0,0};
  byte off = 0;
  byte local = 0;
  for (int i = 0; i <= 6; ++i) {
    offsets[i] = off;
    localoffsets[i] = local;
    Feature feat = featurecollection[i];
    if (feat.size == 32) {
      off = off + (feat.nthres);
    } else {
      local = (feat.size+local) % 8;
      off = off + (feat.size+local) / 8;
    }
    //Serial << "off["<< i << "] " << off << "\n";
  }
  off = 0;
  local = 0;
  for (int i = 0; i <= 4; ++i) {
    // Serial << "nodestoprocess \"" << nodestoprocess << "\" node: \"" << node << "\" nodesOnelevelHigher: " << nodesOnelevelHigher << " node at level to pass " << nodesatlevel << "" << '\n';
    if (4 == i) {
      // Reached a leave
      byte leaveindex = 0;
      if (local == 0) {
        //Serial << "take leave at index " << off << " " << tree[off];
        leaveindex = tree[off];
      } else {
        //Serial << "take leave at index " << off+1 << " " << tree[off+1];
        leaveindex = tree[off+1];
      }
      //Serial << " = " << leaf_values[leaveindex] << "\n";
      // Serial << "Returning: leaveoffset: " << leaveoffset << " numberleave: " << numberleave << " leaf_values: " << leaf_values[numberleave] << '\n';
      return leaf_values[leaveindex];
    }
    byte currentnode = 0;
    if (local == 0) {
      currentnode = tree[off];
    } else {
      // TODO this could be features [offset+1]
      currentnode = getBitsfromTwoBytes(tree[off], tree[off+1], (8-local), (8-local));
      //Serial << "tree[" << off << "] " << tree[off] << " tree[" << off+1 << "] " << tree[off+1] << " local " << local << " currentnode " << currentnode << "\n";
      //byte currentnode = checkifoneortwoBytes(tree[off], tree[off+1], local, local - );
    }
    byte feature = bytetobyterange(currentnode, 8, 8-3);
    Feature currentfeature = featurecollection[feature];
    byte refsize = currentfeature.refsize;
    
    /// TODO calculate the size of reference to feature? need to change trees and therefore the reading of 
    byte findex = bytetobyterange(currentnode, 5, 5-refsize);
    float threshold;
    
    if (localoffsets[feature] == 0) {
      // Serial << "features[offsets[feature]+findex]: " << features[offsets[feature]+findex] << " offsets[feature] " << offsets[feature] << "currentnode" << currentnode << "\n";
      threshold = features[offsets[feature]+findex];
    } else {
      // TODO this could be features [offset+1]
      threshold = checkifoneortwoBytes(features[offsets[feature]+findex], features[offsets[feature]+findex], localoffsets[feature], localoffsets[feature] - currentfeature.size);
    }
    // Serial << "Get feature " << feature << " and x threshold " << findex << " and threshold " << threshold << " comparing input[feature] " <<  input[feature] << "\n";
    byte nodestoprocess = 0;
    byte oldnode = node;
    if (input[feature] <= threshold) {
      node = (node * 2) + 1;
      nodestoprocess = node - oldnode;
      calculateoffset(tree, nodestoprocess, off, local, featurecollection);
      // set off and local to match next node. 
      // Serial << "LEFT: " << "offset " << off << " local: " << local << " node " << node << " oldnode " << oldnode << '\n';
    } else {
      node = (node * 2) + 2;
      nodestoprocess = node - oldnode;
      calculateoffset(tree, nodestoprocess, off, local, featurecollection);
      // set off and local to match next node. 
      // Serial << "RIGHT: " << "offset " << off << " local: " << local << " node " << node << " oldnode " << oldnode << '\n';
    }
  }
  return 0.0;
}
void calculateoffset(byte tree[], byte nodestoprocess, byte &off, byte &local, Feature featurecollection[]){
  byte currentnode;
  // Serial << "processed " << nodestoprocess << " nodes off: " <<  off << " local: " <<  local << "\n";
  for (int j = 0; j < nodestoprocess; j++) {
    if (local == 0) {
      currentnode = tree[off];
    } else {
      currentnode = getBitsfromTwoBytes(tree[off], tree[off+1], (8-local), (8-local));
    }
    byte feature = bytetobyterange(currentnode, 8, 8-3);
    Feature currentfeature = featurecollection[feature];
    byte refsize = currentfeature.refsize;
    
    byte calclocal = 3+refsize;
    off = off + floor((calclocal+local) / 8);  
    byte oldlocal = local;
    local = (calclocal + local) % 8;
  }
  //Serial << "processed " << nodestoprocess << " nodes off: " <<  off << " local: " <<  local << "\n";
}
byte getBitsfromTwoBytes(byte first, byte second, byte start, byte end) {
  byte firstpart = first;
  byte secondpart = second;
  byte refbitsfirstpart = bytetobyterange(firstpart, start, 0);
  byte refbitssecondpart = bytetobyterange(secondpart, 8, end);
  refbitsfirstpart = refbitsfirstpart << 8 - end;
  byte index = refbitsfirstpart + refbitssecondpart;
  return index;
}

void setup() {
  size_t size = BUFFER_SIZE;
  Serial.begin(9600);
  switch (parseInput(size, gpBuffer)) {
    case ERROR_INVALID_ARGUMENT:
      Serial.println("invalid argument");
      break;
    case ERROR_INVALID_INPUT:
      Serial.println("invalid input");
      break;
    case ERROR_FAILED_READ:
      Serial.println("failed to read from serial");
      break;
    case ERROR_OUT_OF_MEMORY:
      Serial.println("input requires too much memory");
      break;
    default:
      break;
  }
}

void loop() {
  while (!Serial.available()) {
    delay(100);
  }
  long overall= 0;
	long randomtime = 0;
	long predicttime = 0;
	unsigned long StartTime = micros();
  unsigned long startreadfeatures; 
  unsigned long endreadfeatures; 
  unsigned long StartRandom;
  unsigned long EndRandom;
  unsigned long startpredict;
  unsigned long endpredict;
  Serial.println("Read Features Time, Predict Time");
  //Serial << "Read Features Time, Predict Time" << "\n";
  for (int x = 0; x <= 20; x++) {
     overall = 0;
	 randomtime = 0;
	 predicttime = 0;
	 StartTime = micros();
   startreadfeatures= 0; 
   endreadfeatures= 0; 
   StartRandom= 0;
   EndRandom= 0;
   startpredict= 0;
   endpredict= 0;
  for (int i = 0; i <= 500; i++) {
		StartRandom = micros();
		randomSeed(i);
		float input[6];
		for (int i = 0; i < 6; i++) {
			input[i] = random(0, 6000);;
		}
		EndRandom = micros();
		randomtime = randomtime + (EndRandom-StartRandom);

    Feature thosefeatures[7];
    byte bitperfeature = 12;
// 000 100 1 1. 0101 --> 1
// 001 1.00 1 00111 --> 4
// 010 100 1 0.0110 --> 6
// 011 1.00 1 00010 --> 8
// 100 100 1 0.0000 --> 10
// 101 100 1 00000 --> 16
// 110 100 1 00000 --> 18
    byte offset = 0;
    startreadfeatures = micros();

    for (int j = 0; j <= 6; j++){
      byte readindex = 0;
      if (j != 0) {
        readindex = floor((j * 12)/8);
      } 
      // Serial << "take index " << readindex << " and ggf. " << readindex+1 << "\n";
      byte number = featurecharac[readindex];
      byte number2 = featurecharac[readindex + 1];
      byte index = 0;
      if (8-offset-3 < 0) {
        index = getBitsfromTwoBytes(number, number2, 8-offset, 8 + (8-offset-3));
      } else {
        index = bytetobyterange(number, 8-offset, 8-offset-3);
      }
      // wenn offset >= 8 wird müssen wir die nächste nummer nehmen 
      byte size = 1;
      bool isfloat = false;
      if (8-offset-6 < 0 & 8-offset-3 < 0) {
        size = bytetobyterange(number2, 8-offset-3, 8-offset-6);
      } else if (8-offset-6 < 0){
        size = getBitsfromTwoBytes(number, number2, 8-offset-3, 8 + (8-offset-6));
      } else {
        size = bytetobyterange(number, 8-offset-3, 8-offset-6);
      }
      if (size == 4){
        size = 32;
        isfloat = true;
      } 
      byte nthres = 0;
      if (8-offset-7 < 0 & 8-offset-7-5 < 0) {
        //Serial << "bytetobyterange(number2, 8 + (8-offset-7), 8 + (8-offset-7-5))" << number2 << " " << 8 + (8-offset-7) << " " <<  8 + (8-offset-7-5) << "\n";
        nthres = bytetobyterange(number2, 8 + (8-offset-7), 8 + (8-offset-7-5));
      } else if (8-offset-7-5 < 0){
        nthres = getBitsfromTwoBytes(number, number2, 8-offset-7, 8 + (8-offset-7-5));
      } else {
        nthres = bytetobyterange(number, 8-offset-7, 8-offset-7-5);
      }

      Feature feature = Feature(index, size, isfloat, nthres+1);
      thosefeatures[j] = feature;
      offset = (offset + 12) % 8;
    }
    endreadfeatures = micros();

    // for (int j = 0; j <= 6; j++){
    //   Serial << " Feature " << thosefeatures[j].tindex << " size " << thosefeatures[j].size << " type " << thosefeatures[j].type << " nthres " << thosefeatures[j].nthres <<  " refsize " << thosefeatures[j].refsize << "\n";
    // }
    startpredict = micros();

    float val0 = evaltree(tree0, input, thosefeatures);
    float val1 = evaltree(tree1, input, thosefeatures);
    float val2 = evaltree(tree2, input, thosefeatures);
    float val3 = evaltree(tree3, input, thosefeatures);
    float finalresult =  1.0f / (1.0f + exp(-1.0 * (val3 + val2 + val1 + val0)));
    endpredict = micros();
		predicttime = predicttime + (endpredict-startpredict);
	}
	unsigned long EndTime = micros();
	overall = EndTime-StartTime;
	//Serial << overall << ", " << randomtime<< ", " << endreadfeatures - startreadfeatures << ", " << predicttime << "\n";
	Serial.print(endreadfeatures - startreadfeatures);
  Serial.print(",");
  Serial.print(predicttime);
  delay(1000); 
  }
  }


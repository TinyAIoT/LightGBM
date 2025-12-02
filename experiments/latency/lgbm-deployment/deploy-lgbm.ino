#include "float16.h"
#include "model.h"
int incomingData = 0;
#define BUFFER_SIZE 1024ul
unsigned char gpBuffer[BUFFER_SIZE];
template <typename T>

Print &operator<<(Print &printer, T value)
{
    printer.print(value);
    return printer;
}

namespace
{
    double model_input[54];

    int num_tree_per_iteration_ = 1;
    int num_iterations = 4;
    int num_iteration_for_pred_ = num_iterations;
}

double PredictRaw(const double *features)
{
    double raw = 0.0;
    // compile-time count
    for (int i = 0; i < num_iteration_for_pred_; ++i)
    {
        for (int k = 0; k < num_tree_per_iteration_; ++k)
        {
            raw += (LightGBM::PredictTreePtr[i * num_tree_per_iteration_ + k])(features);
        }
    }
    // Serial.print(raw);
    return raw;
}

double sigmoid_ = 1.0f;
double ConvertOutput(const double input)
{
    double conv = 0.0;
    conv = 1.0f / (1.0f + exp(-sigmoid_ * input));
    return conv;
}

double PredictTree()
{
    double prediction = 0.0;
    prediction = PredictRaw(model_input);
    prediction = ConvertOutput(prediction);
    return prediction;
}

void setup()
{
    size_t size = BUFFER_SIZE;
    Serial.begin(9600);
}
void loop()
{
    Serial.println("Start Loop");
    for (int k = 0; k <= 20; k++)
    {
        long overall;
        long randomtime = 0;
        long predicttime = 0;
        unsigned long StartTime = micros();
        for (int j = 0; j <= 500; j++)
        {
            unsigned long StartRandom = micros();
            randomSeed(j);
            for (int i = 0; i < 10; i++)
            {
                model_input[i] = random(0, 4000);
                // Serial.println(model_input[i]);
            }
            for (int i = 10; i < 54; i++)
            {
                model_input[i] = random(0, 2);
                // Serial.println(model_input[i]);
            }
            unsigned long EndRandom = micros();
            randomtime = randomtime + (EndRandom - StartRandom);

            unsigned long startpredict = micros();
            float val0 = PredictTree();
            unsigned long endpredict = micros();
            predicttime = predicttime + (endpredict - startpredict);
        }
        unsigned long EndTime = micros();
        overall = EndTime - StartTime;
        Serial.print(overall);
        Serial.print(", ");
        Serial.print(randomtime);
        Serial.print(", ");
        Serial.println(predicttime);
    }

    delay(100);
}


import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchTests, Test, submitTestResult } from "../services/api";
import Header from "@/components/Header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";

const Tests = () => {
  const [tests, setTests] = useState<Test[]>([]);
  const [loading, setLoading] = useState(true);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [showExplanation, setShowExplanation] = useState(false);
  const { levelId, topicId } = useParams<{ levelId: string; topicId: string }>();

  useEffect(() => {
    const loadTests = async () => {
      if (!levelId || !topicId) return;
      
      setLoading(true);
      try {
        const data = await fetchTests(Number(levelId), Number(topicId), 1);
        setTests(data);
      } finally {
        setLoading(false);
      }
    };
    
    loadTests();
  }, [levelId, topicId]);

  const handleNext = () => {
    if (currentQuestion < tests.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
      setSelectedAnswer(null);
      setShowExplanation(false);
    } else {
      toast.success("You've completed all questions!");
    }
  };

  const handleSubmit = () => {
    if (selectedAnswer === null) return;
    
    setShowExplanation(true);
    
    const currentTest = tests[currentQuestion];
    const selectedOption = currentTest.options[selectedAnswer];
    const correctOption = currentTest.options.find(opt => opt.is_correct);
    
    if (!selectedOption || !correctOption) return;
    
    submitTestResult({
      test_id: currentTest.id,
      selected_option_id: selectedOption.id,
      correct_option_id: correctOption.id
    }).catch(console.error);
    
    if (selectedOption.is_correct) {
      toast.success("Correct answer!");
    } else {
      toast.error("Incorrect answer!");
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-950 dark:to-purple-900">
        <Header />
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-600"></div>
        </div>
      </div>
    );
  }

  if (tests.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-950 dark:to-purple-900">
        <Header />
        <div className="container mx-auto py-8 text-center">
          <h2 className="text-2xl font-bold text-purple-900 dark:text-purple-100">
            No tests available
          </h2>
        </div>
      </div>
    );
  }

  const currentTest = tests[currentQuestion];

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-950 dark:to-purple-900">
      <Header />
      <main className="container mx-auto py-8">
        <Card className="max-w-3xl mx-auto">
          <CardHeader>
            <CardTitle className="text-xl font-bold text-purple-900 dark:text-purple-100">
              Question {currentQuestion + 1} of {tests.length}
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="text-lg font-medium">{currentTest.question}</div>
            
            {currentTest.image && (
              <div className="my-4">
                <img src={currentTest.image} alt="Question" className="max-w-full rounded-md" />
              </div>
            )}
            
            <RadioGroup 
              value={selectedAnswer !== null ? selectedAnswer.toString() : undefined}
              onValueChange={(value) => setSelectedAnswer(parseInt(value))}
              className="space-y-3"
            >
              {currentTest.options.map((option, index) => (
                <div key={index} className="flex items-center space-x-2">
                  <RadioGroupItem value={index.toString()} id={`option-${index}`} />
                  <Label htmlFor={`option-${index}`} className="cursor-pointer">{option.option}</Label>
                </div>
              ))}
            </RadioGroup>
            
            {showExplanation && (
              <div className="mt-6 p-4 bg-purple-100 dark:bg-purple-900/40 rounded-md">
                <h3 className="font-semibold mb-2">Explanation:</h3>
                <p>{currentTest.answer_explanation}</p>
              </div>
            )}
            
            <div className="flex justify-between pt-4">
              {!showExplanation ? (
                <Button onClick={handleSubmit} disabled={selectedAnswer === null}>
                  Check Answer
                </Button>
              ) : (
                <Button onClick={handleNext}>
                  {currentQuestion < tests.length - 1 ? "Next Question" : "Finish"}
                </Button>
              )}
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  );
};

export default Tests;

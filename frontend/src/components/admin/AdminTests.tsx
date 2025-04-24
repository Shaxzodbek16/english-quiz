
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { toast } from "sonner";
import { API_BASE_URL, fetchLevels, fetchTopics, Level, Topic } from "@/services/api";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog";

interface TestOption {
  option: string;
  is_correct: boolean;
  id?: number;
}

interface Test {
  id: number;
  level_id: number;
  topic_id: number;
  type_id: number;
  question: string;
  image: string;
  answer_explanation: string;
  options: TestOption[];
  created_at: string;
}

const AdminTests = () => {
  const [tests, setTests] = useState<Test[]>([]);
  const [levels, setLevels] = useState<Level[]>([]);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [editingTest, setEditingTest] = useState<Test | null>(null);
  
  // Form fields
  const [levelId, setLevelId] = useState("");
  const [topicId, setTopicId] = useState("");
  const [typeId, setTypeId] = useState("1");
  const [question, setQuestion] = useState("");
  const [image, setImage] = useState("");
  const [explanation, setExplanation] = useState("");
  const [options, setOptions] = useState<TestOption[]>([
    { option: "", is_correct: true },
    { option: "", is_correct: false },
    { option: "", is_correct: false },
    { option: "", is_correct: false },
  ]);

  useEffect(() => {
    loadMasterData();
    loadTests();
  }, []);

  const loadMasterData = async () => {
    try {
      const [levelsData, topicsData] = await Promise.all([
        fetchLevels(),
        fetchTopics()
      ]);
      
      setLevels(levelsData);
      setTopics(topicsData);
    } catch (error) {
      console.error("Error loading master data:", error);
      toast.error("Failed to load levels and topics");
    }
  };

  const loadTests = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem("access_token");
      const tokenType = localStorage.getItem("token_type") || "Bearer";
      
      const response = await fetch(`${API_BASE_URL}/api/v1/tests/`, {
        headers: {
          "Authorization": `${tokenType} ${token}`,
        },
      });
      
      if (!response.ok) {
        throw new Error(`Failed to fetch tests: ${response.statusText}`);
      }
      
      const data = await response.json();
      setTests(data);
    } catch (error) {
      console.error("Error fetching tests:", error);
      toast.error("Failed to load tests");
    } finally {
      setLoading(false);
    }
  };

  const handleOpenDialog = (test?: Test) => {
    if (test) {
      setEditingTest(test);
      setLevelId(test.level_id.toString());
      setTopicId(test.topic_id.toString());
      setTypeId(test.type_id.toString());
      setQuestion(test.question);
      setImage(test.image);
      setExplanation(test.answer_explanation);
      setOptions(test.options.length > 0 ? test.options : [
        { option: "", is_correct: true },
        { option: "", is_correct: false },
        { option: "", is_correct: false },
        { option: "", is_correct: false },
      ]);
    } else {
      setEditingTest(null);
      setLevelId("");
      setTopicId("");
      setTypeId("1");
      setQuestion("");
      setImage("");
      setExplanation("");
      setOptions([
        { option: "", is_correct: true },
        { option: "", is_correct: false },
        { option: "", is_correct: false },
        { option: "", is_correct: false },
      ]);
    }
    setOpen(true);
  };

  const handleOptionChange = (index: number, value: string) => {
    const newOptions = [...options];
    newOptions[index].option = value;
    setOptions(newOptions);
  };

  const handleCorrectAnswerChange = (index: number) => {
    const newOptions = options.map((opt, idx) => ({
      ...opt,
      is_correct: idx === index
    }));
    setOptions(newOptions);
  };

  const handleDelete = async (id: number) => {
    try {
      const token = localStorage.getItem("access_token");
      const tokenType = localStorage.getItem("token_type") || "Bearer";
      
      const response = await fetch(`${API_BASE_URL}/api/v1/tests/${id}`, {
        method: "DELETE",
        headers: {
          "Authorization": `${tokenType} ${token}`,
        },
      });
      
      if (!response.ok) {
        throw new Error(`Failed to delete test: ${response.statusText}`);
      }
      
      toast.success("Test deleted successfully");
      setTests(tests.filter(test => test.id !== id));
    } catch (error) {
      console.error("Error deleting test:", error);
      toast.error("Failed to delete test");
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("access_token");
      const tokenType = localStorage.getItem("token_type") || "Bearer";
      
      const filteredOptions = options.filter(opt => opt.option.trim() !== "");
      
      if (filteredOptions.length < 2) {
        toast.error("Please provide at least two options");
        return;
      }
      
      if (!filteredOptions.some(opt => opt.is_correct)) {
        toast.error("Please mark at least one option as correct");
        return;
      }
      
      const payload = {
        level_id: parseInt(levelId),
        topic_id: parseInt(topicId),
        type_id: parseInt(typeId),
        question,
        image,
        answer_explanation: explanation,
        options: filteredOptions,
      };
      
      const method = editingTest ? "PUT" : "POST";
      const url = editingTest 
        ? `${API_BASE_URL}/api/v1/tests/${editingTest.id}` 
        : `${API_BASE_URL}/api/v1/tests/`;
      
      const response = await fetch(url, {
        method,
        headers: {
          "Authorization": `${tokenType} ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });
      
      if (!response.ok) {
        throw new Error(`Failed to ${editingTest ? "update" : "create"} test: ${response.statusText}`);
      }
      
      const data = await response.json();
      
      if (editingTest) {
        setTests(tests.map(t => t.id === editingTest.id ? data : t));
        toast.success("Test updated successfully");
      } else {
        setTests([...tests, data]);
        toast.success("Test created successfully");
      }
      
      setOpen(false);
    } catch (error) {
      console.error("Error saving test:", error);
      toast.error(`Failed to ${editingTest ? "update" : "create"} test`);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-xl font-semibold">Manage Tests</h3>
        <Button onClick={() => handleOpenDialog()}>Add New Test</Button>
      </div>
      
      {loading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-600"></div>
        </div>
      ) : (
        <div className="rounded-md border overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>ID</TableHead>
                <TableHead>Question</TableHead>
                <TableHead>Level</TableHead>
                <TableHead>Topic</TableHead>
                <TableHead>Created At</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {tests.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={6} className="text-center py-4">
                    No tests found
                  </TableCell>
                </TableRow>
              ) : (
                tests.map((test) => (
                  <TableRow key={test.id}>
                    <TableCell>{test.id}</TableCell>
                    <TableCell className="max-w-xs truncate">{test.question}</TableCell>
                    <TableCell>{levels.find(l => l.id === test.level_id)?.name || test.level_id}</TableCell>
                    <TableCell>{topics.find(t => t.id === test.topic_id)?.name || test.topic_id}</TableCell>
                    <TableCell>{new Date(test.created_at).toLocaleDateString()}</TableCell>
                    <TableCell>
                      <div className="flex space-x-2">
                        <Button 
                          size="sm" 
                          variant="outline" 
                          onClick={() => handleOpenDialog(test)}
                        >
                          Edit
                        </Button>
                        <Button 
                          size="sm" 
                          variant="destructive" 
                          onClick={() => handleDelete(test.id)}
                        >
                          Delete
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </div>
      )}
      
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="sm:max-w-lg">
          <DialogHeader>
            <DialogTitle>{editingTest ? "Edit Test" : "Add New Test"}</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSubmit}>
            <div className="grid gap-4 py-4">
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                <div className="space-y-2">
                  <label htmlFor="level" className="text-sm font-medium">Level</label>
                  <Select value={levelId} onValueChange={setLevelId} required>
                    <SelectTrigger>
                      <SelectValue placeholder="Select Level" />
                    </SelectTrigger>
                    <SelectContent>
                      {levels.map((level) => (
                        <SelectItem key={level.id} value={level.id.toString()}>
                          {level.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <label htmlFor="topic" className="text-sm font-medium">Topic</label>
                  <Select value={topicId} onValueChange={setTopicId} required>
                    <SelectTrigger>
                      <SelectValue placeholder="Select Topic" />
                    </SelectTrigger>
                    <SelectContent>
                      {topics.map((topic) => (
                        <SelectItem key={topic.id} value={topic.id.toString()}>
                          {topic.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>
              
              <div className="space-y-2">
                <label htmlFor="type" className="text-sm font-medium">Type</label>
                <Select value={typeId} onValueChange={setTypeId} required>
                  <SelectTrigger>
                    <SelectValue placeholder="Select Type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="1">Multiple Choice</SelectItem>
                    <SelectItem value="2">True/False</SelectItem>
                    <SelectItem value="3">Fill in the Blank</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <div className="space-y-2">
                <label htmlFor="question" className="text-sm font-medium">Question</label>
                <Textarea
                  id="question"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  required
                  rows={2}
                />
              </div>
              
              <div className="space-y-2">
                <label htmlFor="image" className="text-sm font-medium">Image URL (optional)</label>
                <Input
                  id="image"
                  value={image}
                  onChange={(e) => setImage(e.target.value)}
                />
              </div>
              
              <div className="space-y-2">
                <label className="text-sm font-medium">Options</label>
                {options.map((option, index) => (
                  <div key={index} className="flex gap-2 items-center">
                    <Input
                      value={option.option}
                      onChange={(e) => handleOptionChange(index, e.target.value)}
                      placeholder={`Option ${index + 1}`}
                      className="flex-1"
                    />
                    <div className="flex items-center">
                      <input
                        type="radio"
                        checked={option.is_correct}
                        onChange={() => handleCorrectAnswerChange(index)}
                        className="mr-2"
                      />
                      <span className="text-xs">Correct</span>
                    </div>
                  </div>
                ))}
              </div>
              
              <div className="space-y-2">
                <label htmlFor="explanation" className="text-sm font-medium">Answer Explanation</label>
                <Textarea
                  id="explanation"
                  value={explanation}
                  onChange={(e) => setExplanation(e.target.value)}
                  rows={3}
                />
              </div>
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setOpen(false)}>
                Cancel
              </Button>
              <Button type="submit">Save</Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default AdminTests;

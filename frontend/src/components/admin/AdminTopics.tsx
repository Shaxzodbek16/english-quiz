
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { toast } from "sonner";
import { fetchTopics, Topic, API_BASE_URL } from "@/services/api";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog";

const AdminTopics = () => {
  const [topics, setTopics] = useState<Topic[]>([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [editingTopic, setEditingTopic] = useState<Topic | null>(null);
  const [name, setName] = useState("");
  const [image, setImage] = useState("");

  useEffect(() => {
    loadTopics();
  }, []);

  const loadTopics = async () => {
    setLoading(true);
    try {
      const data = await fetchTopics();
      setTopics(data);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenDialog = (topic?: Topic) => {
    if (topic) {
      setEditingTopic(topic);
      setName(topic.name);
      setImage(topic.image);
    } else {
      setEditingTopic(null);
      setName("");
      setImage("");
    }
    setOpen(true);
  };

  const handleDelete = async (id: number) => {
    try {
      const token = localStorage.getItem("access_token");
      const tokenType = localStorage.getItem("token_type") || "Bearer";
      
      const response = await fetch(`${API_BASE_URL}/api/v1/topics/${id}`, {
        method: "DELETE",
        headers: {
          "Authorization": `${tokenType} ${token}`,
        },
      });
      
      if (!response.ok) {
        throw new Error(`Failed to delete topic: ${response.statusText}`);
      }
      
      toast.success("Topic deleted successfully");
      setTopics(topics.filter(topic => topic.id !== id));
    } catch (error) {
      console.error("Error deleting topic:", error);
      toast.error("Failed to delete topic");
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("access_token");
      const tokenType = localStorage.getItem("token_type") || "Bearer";
      
      const method = editingTopic ? "PUT" : "POST";
      const url = editingTopic 
        ? `${API_BASE_URL}/api/v1/topics/${editingTopic.id}` 
        : `${API_BASE_URL}/api/v1/topics/`;
      
      const response = await fetch(url, {
        method,
        headers: {
          "Authorization": `${tokenType} ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name, image }),
      });
      
      if (!response.ok) {
        throw new Error(`Failed to ${editingTopic ? "update" : "create"} topic: ${response.statusText}`);
      }
      
      const data = await response.json();
      
      if (editingTopic) {
        setTopics(topics.map(t => t.id === editingTopic.id ? data : t));
        toast.success("Topic updated successfully");
      } else {
        setTopics([...topics, data]);
        toast.success("Topic created successfully");
      }
      
      setOpen(false);
    } catch (error) {
      console.error("Error saving topic:", error);
      toast.error(`Failed to ${editingTopic ? "update" : "create"} topic`);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-xl font-semibold">Manage Topics</h3>
        <Button onClick={() => handleOpenDialog()}>Add New Topic</Button>
      </div>
      
      {loading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-600"></div>
        </div>
      ) : (
        <div className="rounded-md border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>ID</TableHead>
                <TableHead>Name</TableHead>
                <TableHead>Image</TableHead>
                <TableHead>Created At</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {topics.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={5} className="text-center py-4">
                    No topics found
                  </TableCell>
                </TableRow>
              ) : (
                topics.map((topic) => (
                  <TableRow key={topic.id}>
                    <TableCell>{topic.id}</TableCell>
                    <TableCell>{topic.name}</TableCell>
                    <TableCell>
                      {topic.image && (
                        <img 
                          src={topic.image} 
                          alt={topic.name} 
                          className="h-10 w-10 object-cover rounded" 
                        />
                      )}
                    </TableCell>
                    <TableCell>{new Date(topic.created_at).toLocaleDateString()}</TableCell>
                    <TableCell>
                      <div className="flex space-x-2">
                        <Button 
                          size="sm" 
                          variant="outline" 
                          onClick={() => handleOpenDialog(topic)}
                        >
                          Edit
                        </Button>
                        <Button 
                          size="sm" 
                          variant="destructive" 
                          onClick={() => handleDelete(topic.id)}
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
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>{editingTopic ? "Edit Topic" : "Add New Topic"}</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSubmit}>
            <div className="grid gap-4 py-4">
              <div className="space-y-2">
                <label htmlFor="name" className="text-sm font-medium">Name</label>
                <Input
                  id="name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                />
              </div>
              <div className="space-y-2">
                <label htmlFor="image" className="text-sm font-medium">Image URL</label>
                <Input
                  id="image"
                  value={image}
                  onChange={(e) => setImage(e.target.value)}
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

export default AdminTopics;

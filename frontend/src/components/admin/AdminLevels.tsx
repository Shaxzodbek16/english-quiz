
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
import { fetchLevels, Level, API_BASE_URL } from "@/services/api";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog";

const AdminLevels = () => {
  const [levels, setLevels] = useState<Level[]>([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [editingLevel, setEditingLevel] = useState<Level | null>(null);
  const [name, setName] = useState("");
  const [image, setImage] = useState("");

  useEffect(() => {
    loadLevels();
  }, []);

  const loadLevels = async () => {
    setLoading(true);
    try {
      const data = await fetchLevels();
      setLevels(data);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenDialog = (level?: Level) => {
    if (level) {
      setEditingLevel(level);
      setName(level.name);
      setImage(level.image);
    } else {
      setEditingLevel(null);
      setName("");
      setImage("");
    }
    setOpen(true);
  };

  const handleDelete = async (id: number) => {
    try {
      const token = localStorage.getItem("access_token");
      const tokenType = localStorage.getItem("token_type") || "Bearer";
      
      const response = await fetch(`${API_BASE_URL}/api/v1/levels/${id}`, {
        method: "DELETE",
        headers: {
          "Authorization": `${tokenType} ${token}`,
        },
      });
      
      if (!response.ok) {
        throw new Error(`Failed to delete level: ${response.statusText}`);
      }
      
      toast.success("Level deleted successfully");
      setLevels(levels.filter(level => level.id !== id));
    } catch (error) {
      console.error("Error deleting level:", error);
      toast.error("Failed to delete level");
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("access_token");
      const tokenType = localStorage.getItem("token_type") || "Bearer";
      
      const method = editingLevel ? "PUT" : "POST";
      const url = editingLevel 
        ? `${API_BASE_URL}/api/v1/levels/${editingLevel.id}` 
        : `${API_BASE_URL}/api/v1/levels/`;
      
      const response = await fetch(url, {
        method,
        headers: {
          "Authorization": `${tokenType} ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name, image }),
      });
      
      if (!response.ok) {
        throw new Error(`Failed to ${editingLevel ? "update" : "create"} level: ${response.statusText}`);
      }
      
      const data = await response.json();
      
      if (editingLevel) {
        setLevels(levels.map(l => l.id === editingLevel.id ? data : l));
        toast.success("Level updated successfully");
      } else {
        setLevels([...levels, data]);
        toast.success("Level created successfully");
      }
      
      setOpen(false);
    } catch (error) {
      console.error("Error saving level:", error);
      toast.error(`Failed to ${editingLevel ? "update" : "create"} level`);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-xl font-semibold">Manage Levels</h3>
        <Button onClick={() => handleOpenDialog()}>Add New Level</Button>
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
              {levels.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={5} className="text-center py-4">
                    No levels found
                  </TableCell>
                </TableRow>
              ) : (
                levels.map((level) => (
                  <TableRow key={level.id}>
                    <TableCell>{level.id}</TableCell>
                    <TableCell>{level.name}</TableCell>
                    <TableCell>
                      {level.image && (
                        <img 
                          src={level.image} 
                          alt={level.name} 
                          className="h-10 w-10 object-cover rounded" 
                        />
                      )}
                    </TableCell>
                    <TableCell>{new Date(level.created_at).toLocaleDateString()}</TableCell>
                    <TableCell>
                      <div className="flex space-x-2">
                        <Button 
                          size="sm" 
                          variant="outline" 
                          onClick={() => handleOpenDialog(level)}
                        >
                          Edit
                        </Button>
                        <Button 
                          size="sm" 
                          variant="destructive" 
                          onClick={() => handleDelete(level.id)}
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
            <DialogTitle>{editingLevel ? "Edit Level" : "Add New Level"}</DialogTitle>
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

export default AdminLevels;

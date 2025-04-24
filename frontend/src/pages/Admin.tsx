
import { useState } from "react";
import Header from "@/components/Header";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import AdminLevels from "@/components/admin/AdminLevels";
import AdminTopics from "@/components/admin/AdminTopics";
import AdminTests from "@/components/admin/AdminTests";

const Admin = () => {
  const [activeTab, setActiveTab] = useState("levels");

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-950 dark:to-purple-900">
      <Header />
      <main className="container mx-auto py-8">
        <div className="mb-8 text-center">
          <h2 className="mb-2 text-3xl font-bold text-purple-900 dark:text-purple-100">
            Admin Dashboard
          </h2>
          <p className="text-purple-700 dark:text-purple-300">
            Manage your content
          </p>
        </div>

        <Tabs defaultValue="levels" value={activeTab} onValueChange={setActiveTab} className="max-w-5xl mx-auto">
          <TabsList className="grid grid-cols-3 mb-8">
            <TabsTrigger value="levels">Levels</TabsTrigger>
            <TabsTrigger value="topics">Topics</TabsTrigger>
            <TabsTrigger value="tests">Tests</TabsTrigger>
          </TabsList>
          
          <TabsContent value="levels" className="mt-6">
            <AdminLevels />
          </TabsContent>
          
          <TabsContent value="topics" className="mt-6">
            <AdminTopics />
          </TabsContent>
          
          <TabsContent value="tests" className="mt-6">
            <AdminTests />
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
};

export default Admin;

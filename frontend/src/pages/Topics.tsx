
import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchTopics, Topic } from "../services/api";
import Header from "@/components/Header";
import GameCard from "@/components/GameCard";

const Topics = () => {
  const [topics, setTopics] = useState<Topic[]>([]);
  const [loading, setLoading] = useState(true);
  const { levelId } = useParams<{ levelId: string }>();
  const navigate = useNavigate();

  useEffect(() => {
    const loadTopics = async () => {
      setLoading(true);
      try {
        const data = await fetchTopics();
        setTopics(data);
      } finally {
        setLoading(false);
      }
    };
    
    loadTopics();
  }, []);

  const handleSelectTopic = (topicId: number) => {
    navigate(`/tests/${levelId}/${topicId}`);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-950 dark:to-purple-900">
      <Header />
      <main className="container mx-auto py-8">
        <div className="mb-8 text-center">
          <h2 className="mb-2 text-3xl font-bold text-purple-900 dark:text-purple-100">
            Select a Topic
          </h2>
          <p className="text-purple-700 dark:text-purple-300">
            Choose a topic for Level {levelId}
          </p>
        </div>
        
        {loading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-600"></div>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6 p-6 sm:grid-cols-2 lg:grid-cols-4">
            {topics.map((topic) => (
              <div 
                key={topic.id} 
                onClick={() => handleSelectTopic(topic.id)} 
                className="cursor-pointer"
              >
                <GameCard
                  title={topic.name}
                  description={`Topic ${topic.id}`}
                />
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
};

export default Topics;

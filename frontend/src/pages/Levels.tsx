
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { fetchLevels, Level } from "../services/api";
import Header from "@/components/Header";
import GameCard from "@/components/GameCard";
import { useAuth } from "../context/AuthContext";

const Levels = () => {
  const [levels, setLevels] = useState<Level[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const { logout } = useAuth();

  useEffect(() => {
    const loadLevels = async () => {
      setLoading(true);
      try {
        const data = await fetchLevels();
        setLevels(data);
      } finally {
        setLoading(false);
      }
    };
    
    loadLevels();
  }, []);

  const handleSelectLevel = (levelId: number) => {
    navigate(`/topics/${levelId}`);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-950 dark:to-purple-900">
      <Header />
      <main className="container mx-auto py-8">
        <div className="mb-8 text-center">
          <h2 className="mb-2 text-3xl font-bold text-purple-900 dark:text-purple-100">
            Select a Level
          </h2>
          <p className="text-purple-700 dark:text-purple-300">
            Choose a level to begin your journey
          </p>
        </div>
        
        {loading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-600"></div>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6 p-6 sm:grid-cols-2 lg:grid-cols-4">
            {levels.map((level) => (
              <div 
                key={level.id} 
                onClick={() => handleSelectLevel(level.id)} 
                className="cursor-pointer"
              >
                <GameCard
                  title={level.name}
                  description={`Level ${level.id}`}
                />
              </div>
            ))}
          </div>
        )}
      </main>
      
      <div className="fixed bottom-4 right-4">
        <button 
          onClick={logout} 
          className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-full"
        >
          Logout
        </button>
      </div>
    </div>
  );
};

export default Levels;

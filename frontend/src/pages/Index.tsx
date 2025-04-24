import Header from "@/components/Header";
import CardGrid from "@/components/CardGrid";

const Index = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-950 dark:to-purple-900">
      <Header />
      <main className="container mx-auto py-8">
        <div className="mb-8 text-center">
          <h2 className="mb-2 text-3xl font-bold text-purple-900 dark:text-purple-100">
            Welcome to the Game
          </h2>
          <p className="text-purple-700 dark:text-purple-300">
            Select a level to begin your journey
          </p>
        </div>
        <CardGrid />
      </main>
    </div>
  );
};

export default Index;

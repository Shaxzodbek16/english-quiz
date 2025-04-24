
import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface GameCardProps {
  title: string;
  description: string;
  className?: string;
}

const GameCard = ({ title, description, className }: GameCardProps) => {
  return (
    <Card
      className={cn(
        "group relative overflow-hidden rounded-xl border-2 border-purple-200/20 bg-gradient-to-br from-purple-50 to-purple-100/90 p-6 transition-all hover:scale-105 hover:border-purple-300/50 hover:shadow-xl dark:from-purple-950/50 dark:to-purple-900/50",
        className
      )}
    >
      <div className="space-y-2">
        <h3 className="text-xl font-bold text-purple-900 dark:text-purple-100">
          {title}
        </h3>
        <p className="text-sm text-purple-700 dark:text-purple-300">
          {description}
        </p>
      </div>
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-purple-500/10 to-transparent opacity-0 transition-opacity group-hover:opacity-100" />
    </Card>
  );
};

export default GameCard;

export const Button = ({ children, onClick, disabled, type = "button" }) => (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className="p-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-blue-300"
    >
      {children}
    </button>
  );
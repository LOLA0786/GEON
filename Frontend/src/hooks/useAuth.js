// import {createContext, useContext, useState, useEffect } from "react";

// const authContext = createContext();

// export const AuthProvider = ({children}) => {
//     const [user, setUser] = useState("");
//     const [loading, setLoading] = useState(true);

//     const signUp = async ({email, password, firstName, lastName}) => {
//         const response = await fetch("http://localhost:8000/auth/signup", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json",
//             },
//             body: JSON.stringify({
//                 email: email,
//                 password: password,
//                 full_name: firstName + " " + lastName,
//             }),
//         });
//     };

//     return (
//         <authContext.Provider value={{ signUp }}>
//             {children}
//         </authContext.Provider>
//     );
// };

// // export const useAuth = () => useContext(authContext);

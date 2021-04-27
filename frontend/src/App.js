import React from "react"
import ReactDOM from "react-dom"

const useState = React.useState
const useEffect = React.useEffect

// function ExampleComponent() {
//   return (
//     <div>
//       <h1>This is sour app d! </h1>
//       <p>The sky is blue</p>
//     </div>
//   )
// }

// ReactDOM.render(<ExampleComponent />, document.querySelector("#app"))

function App() {
  const [pets, setPets] = useState([])

  // only run once the first time this component is rendered
  useEffect(() => {
    if (localStorage.getItem("examplePetData")) {
      setPets(JSON.parse(localStorage.getItem("examplePetData")))
    }
  }, [])

  // run every time our pet state changes
  useEffect(() => {
    localStorage.setItem("examplePetData", JSON.stringify(pets))
  }, [pets])

  return (
    <>
      <OurHeader />
      <LikeArea />
      <TimeArea />
      <AddPetForm setPets={setPets} />
      <ul>
        {pets.map(pet => (
          <Pet setPets={setPets} id={pet.id} name={pet.name} species={pet.species} age={pet.age} key={pet.id} />
        ))}
      </ul>
      <SetToken />
	  <GetToken />
      <Footer />
    </>
  )
}

function AddPetForm(props) {
  const [name, setName] = useState()
  const [species, setSpecies] = useState()
  const [age, setAge] = useState()

  function handleSubmit(e) {
    e.preventDefault()
    props.setPets(prev => prev.concat({ name, species, age, id: Date.now() }))
    setName("")
    setSpecies("")
    setAge("")
  }

  return (
    <form onSubmit={handleSubmit}>
      <fieldset>
        <legend>Add New Pet</legend>
        <input value={name} onChange={e => setName(e.target.value)} placeholder="Name" />
        <input value={species} onChange={e => setSpecies(e.target.value)} placeholder="species" />
        <input value={age} onChange={e => setAge(e.target.value)} placeholder="age in years" />
        <button>Add Pet</button>
      </fieldset>
    </form>
  )
}

function LikeArea() {
  const [likeCount, setLikeCount] = useState(0)

  function increaseLikeHandler() {
    setLikeCount(function (prev) {
      return prev + 1
    })
  }

  function decreaseLikeHandler() {
    setLikeCount(prev => {
      if (prev > 0) {
        return prev - 1
      }
      return 0
    })
  }

  return (
    <>
      <button onClick={increaseLikeHandler}>Increase likes</button>
      <button onClick={decreaseLikeHandler}>Decrease likes</button>
      <h2>This page has been liked {likeCount} times.</h2>
    </>
  )
}

function Pet(props) {
  function handleDelete() {
    props.setPets(prev => prev.filter(pet => pet.id != props.id))
  }

  return (
    <li>
      {props.name} is a {props.species} and is {props.age} years old.
      <button onClick={handleDelete}>Delete</button>
    </li>
  )
}

function Footer() {
  return <small>Copyright Footer Text</small>
}

function SetToken() {
  const [jsonResult, setJsonResult] = useState("No Token")

  function updateJson() {
	fetch("/setToken").then(response =>
      response
        .json()
        .then(data => ({
          data: data,
          status: response.status
        }))
        .then(res => {
          setJsonResult(res.data.token)
        })
    )
  }
  return (
    <>
      <button onClick={updateJson}>Update Token</button>
      <h1>The Token Result is "{jsonResult}"</h1>
    </>
  )
}


function GetToken() {
  const [tokenResult, setTokenResult] = useState("")

  function getToken() {
    //fetch("https://blueprint1.azurewebsites.net/getjson").then(response =>
	fetch("/getToken").then(response =>
      response
        .json()
        .then(data => ({
          data: data,
          status: response.status
        }))
        .then(res => {
          setTokenResult(res.data.token)
        })
    )
  }
  return (
    <>
      <button onClick={getToken}>Get Token</button>
      <h1>The Token Result is "{tokenResult}"</h1>
    </>
  )
}


function TimeArea() {
  const [theTime, setTheTime] = useState(new Date().toLocaleString())

  useEffect(() => {
    const interval = setInterval(() => setTheTime(new Date().toLocaleString()), 1000)

    return () => {
      clearInterval(interval)
    }
  }, [])

  return <p>The current time is {theTime}.</p>
}

function OurHeader() {
  return <h1 className="special">Our Amazing App Header</h1>
}

export default App;


import { useState } from 'react';
import './App.css';

let i = 1;

let g = 1;

function App () {
  const [Boards, setBoards] = useState([])

  const [currentBoard, setCurrentBoard] = useState(null);
  const [currentItem, setCurrentItem] = useState(null)
  const [inputOne, setInputOne] = useState('');
  const [inputItem, setInputItem] = useState('');

  function DragOverHandler(e){
    e.preventDefault();
    if (e.target.className === "item"){
      e.target.style.borderBottom = '100px solid aliceblue'
      
    }
    
  }

  function DragLeaveHandler(e){
    e.target.style.borderBottom = 'none';
    
    
  }

  function DragStartHandler(e, board, item){
    setCurrentBoard(board);
    setCurrentItem(item);
  }

  function DragEndHandler(e){
    e.target.style.borderBottom = 'none';
    //a
    
    
  }

  function dropHandler(e, board, item){
    e.preventDefault();
    e.stopPropagation()
    const currentIndex = currentBoard.items.indexOf(currentItem);
    currentBoard.items.splice(currentIndex, 1);
    const dropIndex = board.items.indexOf(item);
    board.items.splice(dropIndex + 1, 0, currentItem);
    setBoards(Boards.map(b => {
      if(b.id === board.id){
        return board;
      }
      if (b.id === currentBoard.id){
        return currentBoard;
      }
      return b;
    }
    ))
    e.target.style.borderBottom = 'none';
    
  }

  function dropCardHandler(e, board){
    
    board.items.push(currentItem);
    const currentIndex = currentBoard.items.indexOf(currentItem);
    currentBoard.items.splice(currentIndex, 1);
    setBoards(Boards.map(b => {
      if(b.id === board.id){
        return board;
      }
      if (b.id === currentBoard.id){
        return currentBoard;
      }
      return b;
    }))
    
  }
  
  function addTodo(title) {
      setBoards([
        ...Boards,
        {
          id: i, title:title, items: [], plus_button: <div className='plus'></div>
        }
      ])
      i+=1;
      setInputOne((''));
  }

  function addNewItem (item, id) {
    if (item !== '') {
        const newItem = {
            id: g,
            title: item.toString(),
            delete: <div className='delete'></div>
        }
        setCurrentBoard([...Boards, Boards[id - 1].items.push(newItem)]);
        g+=1;
    }
    setInputItem((''));
  }

  

  function DeleteItem(e, board, item) {
   try{
    setCurrentBoard(board);
    setCurrentItem(item);
    const Index = currentBoard.items.indexOf(currentItem);
    currentBoard.items.splice(Index, 1);
    
    setBoards(Boards.map(b=>{
      if (b.id == board.id){
        return board;
      }
      if (b.id === currentBoard.id){
        return currentBoard;
      }
      return b;
    }))
  }
  catch(e){
    
  }
  }

  

  return (
    <div className="App">
      
      {Boards.map((board, index) => 
        <div className='board'
        onDragOver={(e) => DragOverHandler(e)}
        onDrop={(e) => dropCardHandler(e,board)}>
          <div className='board__title'>{board.title}</div>
          {board.items.map(item => 
            <div 
            onDragOver={(e) => DragOverHandler(e)}
            onDragLeave={(e) => DragLeaveHandler(e)}
            onDragStart={(e) => DragStartHandler(e,board,item)}
            onDragEnd={(e)=>DragEndHandler(e)}
            onDrop={(e)=>dropHandler(e, board, item)}
            className="item"
            draggable={true}
            >
              {item.title}
              <div className='delete_item'  onClick={(e) => DeleteItem(e, board, item)}>{item.delete}</div>
            </div> 
          )}
          <div id={board.id} className="list__input"><input type="text" className={board.id} name="newList" value={inputItem} onChange={(event) => setInputItem(event.target.value)} id="newList" placeholder="list name"/>
          <div className='plus__kontainer' onClick={()=>addNewItem(inputItem, board.id)} >{board.plus_button}</div></div>
        </div>
      )}
      <div class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h4 class="modal-title">Введите новый лист</h4>
            </div>
            <div class="modal-body">
                <input type="text" name="newList" value={inputOne} onChange={(event) => setInputOne(event.target.value)} id="newList"/>
            </div>
            <div class="modal-footer">
                <button class="accept__button" onClick={()=>addTodo(inputOne)}>Добавить</button>
            </div>
            </div>
        </div>
    </div>
  );
}

export default App;
